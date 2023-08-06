from imgtec.console.breakpoints import clear
from imgtec.console.support import *
from imgtec.console.generic_device import thread
from imgtec.lib import rst
from imgtec.lib.ordered_dict import OrderedDict

create = named('create')

actions = [
    (create,   'create'),
    (clear,    'clear'),
]

class TeamDict(OrderedDict):
    titles = ['Team Name', 'Members']

    def __repr__(self, **kwargs):
        if self:
            vals = []
            for name, members in self.items():
                vals.append((name, ', '.join(x.name for x in members)))
            return rst.simple_table(self.titles, vals)
        else:
            return 'No Teams'
            
def _get_teams(tiny):
    teams = tiny.ListTeams()
    res = TeamDict()
    for team_id, members in teams.items():
        d = []
        for member in members:
            m = re.match(r's(\d+)c(\d+)[tv](\d+)', member)
            indexes = [int(x) for x in m.group(1, 2, 3)]
            d.append(thread(*indexes))
        res[team_id] = d
    return res


@command(action=actions,
         team_name=[named_all])
def team(action=None, team_name=None, devices=[]):
    """Create or remove Teams.

    This command creates, edits or removes teams from the probe, then returns 
    the resulting list of teams as a dictionary of team-id->[members].
    
    Teams allow hardware threads and cores to be started and halted together. 
    Once a thread is a member of a team then a run of any thread in that team 
    will cause all team members to run.  Similarly if any thread should halt 
    (either because of an explicit stop command or a breakpoint is hit) then all 
    other team members will stop (they will have a runstate of 'stopped').

    To use, first create a team containing the desired members.  It is 
    a requirement that no thread can be a member of more than one team, this 
    command will fail if that requirement is not met.

    For example:

    ================================= =======================================
    Syntax                            Description
    ================================= =======================================
    team()                            List teams
    team(create, s0c0v0, s0c1)        Create a team.
    team(clear, "team1")              Remove the team named "team1".
    team(clear, all)                  Remove all teams.
    ================================= =======================================

    """
    
    tiny = devices[0].probe.tiny
    
    if action is None:
        if len(devices) > 1:
            raise RuntimeError('Specify create to create a team. e.g. team(create, device[, device[,...]])')
    elif action == 'create':
        if team_name:
            raise RuntimeError('You cannot specify a team name when creating a team')
        
        teams = _get_teams(tiny)
        membership = {}
        for tmid, members in teams.items():
            for m in members:
                membership[m.name] = tmid 
        members = [d.name for d in devices]
        already = [(m, membership[m]) for m in members if m in membership]
        if already:
            already = '\n  '.join(['%s is already in %s' % x for x in already])
            raise RuntimeError('Threads cannot be members of more than one team.\n  ' + already)
        
        tiny.CreateTeam(members)
    elif action == 'clear':
        tiny.DeleteTeam(team_name)
    else:
        raise ValueError('Invalid action')

    return _get_teams(tiny)
