#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 18:24:45 2017

@author: jmmauricio
"""

import numpy as np
from pydgrid.electric import bess_vsc, bess_vsc_eval
from pydgrid.pf import pf_eval

import numba

class simu(object):  # feed mode
    
    def __init__(self,data_input,grid=0):

        if type(data_input) == str:
            json_file = data_input
            self.json_file = json_file
            self.json_data = open(json_file).read().replace("'",'"')
            data = json.loads(self.json_data)
        elif type(data_input) == dict:
            data = data_input
            self.data = data
        
        self.Dt = 0.1  # integraation step size
        self.N_x = 0
        ix_0 = 0
        
        # bess_vsc_feeder
        obj_bess_vsc = bess_vsc(data_input,grid)
        for item in obj_bess_vsc.params_bess_vsc:
            item['ix_0'] = ix_0
            ix_0 += item['N_x']
 
        N_x = ix_0
        
        dtype = np.dtype([('Dt', 'float64'),
                          ('N_x','int64'),
                          ('N_steps','int32'),
                          ('x',np.float64,(N_x,1)),('f',np.float64,(N_x,1)),('h',np.float64,(N_x,1)),
                          ('N_bess_vsc_feeder','int32')
                 ])
                     
        element_list = []
        
        element_list += [(self.Dt, # Dt
                          N_x, # N_x
                          0, # N_steps 
                          np.zeros((N_x,1)),np.zeros((N_x,1)),np.zeros((N_x,1)),   # x, f, h
                          len(obj_bess_vsc.params_bess_vsc)
                          )] 
    
        self.params_simu= np.rec.array(element_list,dtype=dtype)
        self.params_bess_vsc = obj_bess_vsc.params_bess_vsc
#        self.N_x = N_x

#@numba.jit(nopython=True,cache=True)    
def ini_eval(t,
           params_pf,
           params_simu,
           params_bess_vsc):
        
    # bess_vsc
    bess_vsc_eval(t,1,params_bess_vsc,params_pf,params_simu)




#@numba.jit(nopython=True,cache=True)    
def f_eval(t,
           params_pf,
           params_simu,
           params_bess_vsc):
    
    # update elements derivatives:
    bess_vsc_eval(t,2,params_bess_vsc,params_pf,params_simu)
        

         
    
#@numba.jit(nopython=True,cache=True,nogil=True)    
def run_eval(t_end,
             params_pf,
             params_simu,
             params_bess_vsc):

    N_v = params_pf[0].N_nodes_v
    N_i = params_pf[0].N_nodes_i
    N_x = params_simu[0].N_x

    N_nodes = int(N_v + N_i)    
    N_steps = int(np.ceil(t_end/params_simu[0].Dt) ) 
    T = np.zeros((N_steps,1), dtype=np.float64)                # time ouput 
    V_nodes = np.zeros((N_steps,N_nodes), dtype=np.complex128) # voltages ouputs 
    I_nodes = np.zeros((N_steps,N_nodes), dtype=np.complex128) # currents ouputs 
    X = np.zeros((N_steps,N_x), dtype=np.float64) # currents ouputs 
    for it in range(N_steps):
        t = params_simu[0].Dt*it
        f_eval(t,
               params_pf,
               params_simu,
               params_bess_vsc)
        # ode solver        
        params_simu[0].x[:] += params_simu[0].Dt*params_simu[0].f    

        
        # update elements outputs:
        bess_vsc_eval(t,4,params_bess_vsc,params_pf,params_simu)

        # update power flow
        V_node, I_node = pf_eval(params_pf)
       
        # outputs update
        T[it,0] = t
        V_nodes[it,:] = V_node[:,0]
        I_nodes[it,:] = I_node[:,0]
        X[it,:] = params_simu[0].x[:,0]        
    params_simu[0].N_steps = N_steps    

    return T,V_nodes,I_nodes,X

    