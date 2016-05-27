#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import random
import sys


MAX_COUNT = 10000000  # Upper limit for simulation termination


def simulate(l, k):
    """
    μα = 4
    μβ = 1
    l = λ
    k = threshold
    """
    print 'l = {}\nk = {}'.format(l, k)
    j = k+11  # total possible states of given system
    state = 0  # States of system go from 0 to j. We start from 0
    p = [0]*j  # list of probabilities for every state
    total_arrivals = 0  # total arrivals
    arrivals = [0]*j  # list of total arrivals for every state
    lm1 = l/(l+4)  # λ/(λ+μα)
    lm2 = l/(l+4+1)  # λ/(λ+μα+μβ)
    lm3 = (l+4)/(l+4+1)  # (λ+μα)/(λ+μα+μβ)
    lm4 = l/(l+1)  # λ/(λ+μβ)
    count = 0  # total transitions
    eps = 1  # convergence criteria
    current = 0  # current avg customers
    previous = 0  # previous avg customers
    ga = 0  # throughput of A
    gb = 0  # throughput of B

    # End simulation when MAX_COUNT is exceeded or when consecutive client
    # avgerage client differ less than 0.0001 and we have convergence.
    while count < MAX_COUNT and eps > 0.0001:
        for i in range(1000):
            if state == 0:
                # Only arrival is possible in state 0
                total_arrivals += 1
                arrivals[state] += 1
                state += 1
                count += 1
            elif state <= k:
                # B is idle. Only A is operational
                if random.uniform(0, 1) < lm1:
                    # random < λ/(λ+μα)) -> arrival
                    total_arrivals += 1
                    arrivals[state] += 1
                    if state == k:
                        # if we're at k state, it's time for B to stop
                        # idling so we move to 2k + 1 state
                        state = 2*k+1
                    else:
                        state += 1
                        count += 1
                else:
                    # departure
                    state -= 1
                    count += 1
            elif state == k+1:
                # Only B operational
                if random.uniform(0, 1) < lm4:
                    # random < λ/(λ+μβ) -> arrival
                    total_arrivals += 1
                    arrivals[state] += 1
                    state += 1
                    count += 1
                else:
                    # departure
                    state = 0
                    count += 1
            elif k+2 <= state <= 2*k+1:
                # Both A and B operational. After departure either A or B start
                # idling.
                random_value = random.uniform(0, 1)
                if random_value < lm2:
                    # random < λ/(λ+μα+μβ)) -> arrival
                    total_arrivals += 1
                    arrivals[state] += 1
                    if state < k + 10:
                        state += 1
                    count += 1
                elif random_value < lm3:
                    # random < (λ+μα)/(λ+μα+μβ)) -> departure from A
                    state -= 1
                    count += 1
                else:
                    # departure from B
                    state = state - k - 1
                    count += 1
            else:
                # Both A and B operational. After departure both remain
                # operational
                if random.uniform(0, 1) < lm2:
                    # random < λ/(λ+μα+μβ) -> arrival
                    if state == k+10:
                        # final state
                        total_arrivals += 1
                        arrivals[state] += 1
                        count += 1
                    else:
                        total_arrivals += 1
                        arrivals[state] += 1
                        state += 1
                        count += 1
                else:
                    # departure
                    state -= 1
                    count += 1

        for i in range(j):
            p[i] = arrivals[i]/total_arrivals

        previous = current

        # Calculate avg num of clients in our queuing system
        # Avg num of clients is calculated via:
        #     Σ(i*p[i]) (0<=i<=k) + p[k+1] + Σ((i-k)*p[i]) (k+2<=i<j)
        avg = 0
        for i in range(k+1):
            # for i in [0, k] we have i clients in the system with p[i]
            # probability for each state
            avg += i*p[i]
        avg += p[k+1]  # in k+1 state we only have 1 client in B
        for i in range(k+2, j):
            # for i in [k+2, k+11) we have i-k clients in our system with p[i]
            # probability for each state
            avg += (i-k)*p[i]

        current = avg
        print current
        eps = abs(current-previous)
        if count == 1000:
            # For the first 1000 events we are in a transient state.
            # We re-initialize the arrivals and total_arrivals
            arrivals = [0]*j
            total_arrivals = 0

    # Below this point we have convergence
    print '\n\n'
    for i in range(j):
        # print probabilities for every state
        print 'p[{}]={}'.format(i, p[i])
    print 'count = {}\n\n'.format(count)

    for i in range(1, j):
        # A is active in all states but 0 and k+1
        ga = ga+p[i]
    ga = ga-p[k+1]
    ga = 4*ga

    for i in range(k+1, j):
        # B is active in states k+1 to j (k+11)
        gb = gb+p[i]
    gb = 1*gb

    g = ga/gb if gb > 0 else 'INF'

    print 'ga = {}\ngb = {}\ng = {}\n'.format(ga, gb, g)


if __name__ == '__main__':
    if len(sys.argv) == 1 or 'help' in sys.argv:
        print 'Usage:\n {} l(=1,2,3) k(=1,2,...,9)\n'.format(sys.argv[0])
        sys.exit(0)
    elif len(sys.argv) != 3:
        print 'Error. Exactly 2 arguments are required.\n' +\
            'Example: ./simulation.py 2 7'
        sys.exit(1)
    simulate(float(sys.argv[1]), int(sys.argv[2]))
