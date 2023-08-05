#!/usr/bin/env python

import radical.pilot as rp

session = rp.Session()

try:
    pd = rp.ComputePilotDescription()
    pd.resource      = 'xsede.comet_ssh'
    pd.cores         = 16
    pd.runtime       = 10
    pd.queue         = 'debug'
    pd.project       = "TG-MCB090174"
    pd.access_schema = "gsissh"
    
    ud = rp.ComputeUnitDescription()
    ud.executable    = "pmemd.MPI"
    ud.pre_exec      = ['module load amber']
    ud.arguments     = '-O -i mdin -c inpcrd -p prmtop -o mdout.out'.split()
    ud.cores         = 2
    ud.mpi           = True

    pmgr  = rp.PilotManager(session)
    pilot = pmgr.submit_pilots(pd)
    umgr  = rp.UnitManager(session)
    units = umgr.submit_units([ud])

    umgr.add_pilots(pilot)
    umgr.wait_units()

finally:
    session.close()


