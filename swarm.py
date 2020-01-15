# Ronald Randolph
# CS420: Biologically - Inspired Computation
# Particle Swarm Optimization Algorithm
#--- IMPORT DEPENDENCIES ------------------------------------------------------+

from __future__ import division
import random
import math

#--- VARIABLE FUNCTION DEFINITIONS --------------------------------------------+

def mdist(xmax, ymax):
    retv = math.sqrt((xmax**2) + (ymax**2)) / 2
    return retv

def pdist(coord):
    retv = math.sqrt(((coord[0] - 20)**2) + ((coord[1] - 7)**2))
    return retv

def ndist(coord): 
    retv = math.sqrt(((coord[0] + 20)**2) + ((coord[1] + 7)**2))
    return retv

#--- PROBLEM FUNCTION ---------------------------------------------------------+

# function for problem 1
def func1(coord):
    retv = 100 * (1 - (pdist(coord) / mdist(50,50)))
    return retv

# function for problem 2
def func2(coord):
    retv = 9 * max(0,(10 - (pdist(coord)**2))) 
    retv += 10 * (1 - (pdist(coord) / mdist(50,50)))
    retv += 70 * (1 - (ndist(coord) / mdist(50,50)))
    return retv 

#--- MAIN ---------------------------------------------------------------------+

class Particle:
    def __init__(self):
        self.position_i=[]          # particle position
        self.velocity_i=[]          # particle velocity
        self.pos_best_i=[]          # best position individual
        self.err_best_i=-1          # best error individual
        self.err_i=-1               # error individual

        #initialize velocity to 0 and position randomly
        for i in range(0,num_dimensions):
            self.velocity_i.append(0.0)
            self.position_i.append(random.randint(-50,50))

        #print(self.velocity_i)
        #print(self.position_i)
        #print("\n")

    # evaluate current fitness
    def evaluate(self,costFunc):
        self.err_i=costFunc(self.position_i)

        # check to see if the current position is an individual best
        if self.err_i > self.err_best_i or self.err_best_i==-1:
            self.pos_best_i=self.position_i.copy()
            self.err_best_i=self.err_i
                    
    # update new particle velocity
    def update_velocity(self,pos_best_g):
        w=0.6      # constant inertia weight (how much to weigh the previous velocity)
        c1=2        # cognative constant
        c2=4     # social constant
        
        for i in range(0,num_dimensions):
            r1=random.random()
            r2=random.random()
            
            vel_cognitive=c1*r1*(self.pos_best_i[i]-self.position_i[i])
            vel_social=c2*r2*(pos_best_g[i]-self.position_i[i])
            self.velocity_i[i]=w*self.velocity_i[i]+vel_cognitive+vel_social

    # update the particle position based off new velocity updates
    def update_position(self,bounds):
        for i in range(0,num_dimensions):
            self.position_i[i]=self.position_i[i]+self.velocity_i[i]
            
            # adjust maximum position if necessary
            if self.position_i[i]>bounds[i][1]:
                self.position_i[i]=bounds[i][1]

            # adjust minimum position if neseccary
            if self.position_i[i]<bounds[i][0]:
                self.position_i[i]=bounds[i][0]
        
class PSO():
    def __init__(self, costFunc, bounds, num_particles, maxiter, verbose=False):
        global num_dimensions

        num_dimensions=2                # num of dimensions
        err_best_g=-1                   # best error for group
        pos_best_g=[]                   # best position for group

        # establish the swarm
        swarm=[]
        for i in range(0,num_particles):
            swarm.append(Particle())

        # begin optimization loop
        i=0
        cont = True
        while i<maxiter and cont:
            if verbose: print(f'iter: {i:>4d}, best solution: {err_best_g:10.6f}')
            
            e_xSum = 0.0
            e_ySum = 0.0
            nConv = 0

            # cycle through particles in swarm and evaluate fitness
            for j in range(0,num_particles):
                swarm[j].evaluate(costFunc)

                # determine if current particle is the best (globally)
                if swarm[j].err_i > err_best_g or err_best_g==-1:
                    pos_best_g=list(swarm[j].position_i)
                    err_best_g=float(swarm[j].err_i)
                
                # sum positional error of swarm
                e_xSum += pow((swarm[j].position_i[0] - pos_best_g[0]),2)
                e_ySum += pow((swarm[j].position_i[1] - pos_best_g[1]),2)

                #get distance from global best position
                distance = math.sqrt(((swarm[j].position_i[0] - pos_best_g[0])**2)+((swarm[j].position_i[1] - pos_best_g[1])**2))
                if distance <= 3:
                    nConv += 1
            
            # calculate average coordinate error of swarm
            error_x = math.sqrt((1/(2*num_particles)) * e_xSum)
            error_y = math.sqrt((1/(2*num_particles)) * e_ySum)
            pConv = float(nConv / num_particles)

            # check stopping condition #1
            print(pConv)
            if error_x < 0.01 and error_y < 0.01:
                cont = False

            # cycle through swarm and update velocities and position
            for j in range(0,num_particles):
                swarm[j].update_velocity(pos_best_g)
                swarm[j].update_position(bounds)
            
            i+=1

        # print final results
        print('\nFINAL SOLUTION:')
        print(f'   > {pos_best_g}')
        print(f'   > {err_best_g}\n')

#--- RUN ----------------------------------------------------------------------+

bounds=[(-50,50),(-50,50)]  # input world bounds [(x1_min,x1_max),(x2_min,x2_max)...]
PSO(func2, bounds, num_particles = 30, maxiter=50, verbose=False)

#--- END ----------------------------------------------------------------------+