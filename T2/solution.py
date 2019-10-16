#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the homework.

#   You may add only standard python imports---i.e.
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files
#   Runs this file requiere numpy library and python 3.6 or higher

import os #for time functions
import math
from search import * #for search engines
from sliders import *
from problems import *


#SLIDERS HEURISTICS
def sliders_h_zero(state):
    return 0


def sliders_h_basic(state):
    sum_in_width = 0
    sum_in_height = 0
    for width in range(state.tiles.shape[0]):
        correlative = np.arange(np.min(state.tiles[width]), np.min(state.tiles[width])+state.tiles.shape[1], 1)
        if np.array_equal(state.tiles[width], correlative) is False:
            sum_in_width += 1
    for height in range(state.tiles.shape[1]):
        correlative = np.arange(np.min(state.tiles[:,height]), state.tiles.shape[1]+np.min(state.tiles[:,height])+1, state.tiles.shape[1] )
        if np.array_equal(state.tiles[:,height], correlative) is False :
            sum_in_height += 1

    return min(sum_in_width,sum_in_height)  


def sliders_h_alternate(state):
#IMPLEMENT
#----------------------------------------------
    '''a better heuristic'''
    '''INPUT: a sliders state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''

    slide_mh = 0
    incorrect = 0
    for row in range(state.height):
        for col in range(state.width):
            number = state.tiles[row][col]
            x = number % state.width
            y = number // state.width
            x_distance = abs(x - col)
            y_distance = abs(y - row)
            if x_distance + y_distance:
                incorrect += 1
            x_delta = min(x_distance, state.width - x_distance)
            y_delta = min(y_distance, state.height - y_distance)
            slide_mh += x_delta + y_delta
    if incorrect:
        return slide_mh / incorrect
    return 0


def fval_function(sN, weight):
    """
    Provide a custom formula for f-value computation for Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SlidersState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
  
    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    #print(sN.gval, sN.hval, sN.gval + weight*sN.hval )
    return sN.gval + weight*sN.hval


def weighted_astar(initial_state, heur_fn, weight=1., timebound = 10):
    '''Provides an implementation of weighted a-star'''
    '''INPUT: a sliders state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''

    wa_se = SearchEngine('custom', 'full')
    wa_se.trace_on(0)
    wa_se.init_search(initial_state, sliders_goal_state, heur_fn, (lambda sN: fval_function(sN, weight)))
    result = wa_se.search(timebound=timebound)

    if result:
        return result
    else:
        return False


def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 10):
    #IMPLEMENT
    #----------------------------------------------
    '''Provides an implementation of anytime weighted a-star (AWA*), as described in the Homework'''
    '''INPUT: a sliders state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of anytime weighted astar algorithm'''

    awa_se = SearchEngine('custom', 'full')
    awa_se.trace_on(0)
    awa_se.init_search(initial_state, sliders_goal_state, heur_fn,
                       (lambda sN: fval_function(sN, weight)))
    result = awa_se.search(timebound=timebound)
    current_solution = result
    while result:
        result = awa_se._searchOpen(
            sliders_goal_state, heur_fn,
            (lambda sN: fval_function(sN, weight)),
            [float('inf'), float('inf'), current_solution.gval])
        if result:
            current_solution = result.state
    result = current_solution
    return result


def restarting_weighted_astar(initial_state, heur_fn, weight=1., phi=0.8, timebound = 10):
    #IMPLEMENT
    #----------------------------------------------
    '''Provides an implementation of RWA*, as described in the homework'''
    '''INPUT: a sliders state that represents the start state, an heuristic function, an initial weight, a phi parameter and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of restarting weighted astar algorithm'''

    current_weight = weight
    rwa_se = SearchEngine('custom', 'full')
    rwa_se.trace_on(0)
    rwa_se.init_search(initial_state, sliders_goal_state, heur_fn,
                       (lambda sN: fval_function(sN, current_weight)))
    result = rwa_se.search(timebound=timebound)
    current_solution = result
    while result and (current_weight > 1):
        current_weight = max(1, phi * current_weight)
        timebound -= (os.times()[0] - rwa_se.search_start_time)
        rwa_se.init_search(initial_state, sliders_goal_state, heur_fn,
                           (lambda sN: fval_function(sN, current_weight)))
        result = rwa_se.search(
            timebound=timebound,
            costbound=[float('inf'), float('inf'), current_solution.gval])
        if result:
            current_solution = result
    result = current_solution
    return result


if __name__ == "__main__":

    #sample runs 
    se = SearchEngine('astar', 'full')

    #If you want to trace the search, set trace_on.  Using Level 1 for illustration. Level 2 prints more detailed results.    
    se.trace_on(0)
    #se.trace_on(1)
    #se.trace_on(2)

    s0 = PROBLEMS[7]
    s_easy = PROBLEMS[2]
    s_mid = PROBLEMS[6]
    s_hard = PROBLEMS[10]

    print("=========Test 1. Astar with h_alternate heuristic========")
    se.init_search(s0, sliders_goal_state, sliders_h_alternate)
    final = se.search(timebound=20)
    if final: final.print_path()
    print("===================================================")

    print("=========Test 2. Weighted Astar with h_alternate heuristic========")
    weight = 10
    final = weighted_astar(s0, heur_fn=sliders_h_alternate, weight=weight,
                           timebound=20)
    if final: final.print_path()
    print("===================================================")

    print("=========Test 3. Anytime Weighted Astar with h_alternate heuristic========")
    weight = 10
    final = anytime_weighted_astar(s0, heur_fn=sliders_h_alternate,
                                      weight=weight, timebound=20)
    if final: final.print_path()
    print("===================================================")

    print("=========Test 4. Restarting Weighted Astar with h_alternate heuristic========")
    weight = 10
    final = restarting_weighted_astar(s0, heur_fn=sliders_h_alternate,
                                      weight=weight, timebound=20)
    if final: final.print_path()
    print("===================================================")

    print("=========Demo 1. Astar with h_zero heuristic========")
    se.init_search(s0, sliders_goal_state, sliders_h_zero)
    final = se.search(timebound=20)
    if final: final.print_path()
    print("===================================================")

    print("=========Demo 2. Astar with h_basic heuristic========")
    se.init_search(s0, sliders_goal_state, sliders_h_basic)
    final = se.search(timebound=20)
    if final: final.print_path()
    print("===================================================")

    print("=========Demo 3. Weighted Astar with h_basic heuristic========")
    weight = 10
    final = weighted_astar(s0, heur_fn=sliders_h_basic, weight=weight, timebound=20)
    if final: final.print_path()
    print("===================================================")
