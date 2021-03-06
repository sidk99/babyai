
import gym
from gym_minigrid.envs import Key, Ball, Box
from .verifier import *
from .levelgen import *
from gym_minigrid.minigrid import *
from gym_minigrid.roomgrid import *
class GoalColor(WorldObj):
    def __init__(self, color):
        super().__init__('box', color)

    def can_overlap(self):
        return True

    def render(self, img):
        fill_coords(img, point_in_rect(0, 1, 0, 1), COLORS[self.color])

class ProofTest(RoomGridLevel):
    """
    Go to the red doorThree
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None, doors_per_side=3, instrs=None, start_room=0, args=None, steps_limit=50, step_reward=-0.01):
        self.doors_per_side=doors_per_side-1
        self.door_pos_lst = args['door_pos_lst']
        self.door_color_lst = args['door_color_lst']
        self.door_lock_lst = args['door_lock_lst']
        self.room_objects = args['room_objects']
        self.room_objects_color = args['room_objects_color']
        self.width=args['width']
        self.height=args['height']
        self.start_room = start_room
        self.steps_limit= steps_limit
        self.step_reward = step_reward
        self.instrs = instrs
        super().__init__(
            num_rows=1,
            num_cols=4,
            room_size=5,
            seed=seed
        )

    def _gen_grid(self, width, height):
        # Create the grid
        self.grid = Grid(width, height)

        self.room_grid = []
        # For each row of rooms
        for j in range(0, self.num_rows):
            row = []

            # For each column of rooms
            for i in range(0, self.num_cols):
                room = Room(
                    (i * (self.room_size-1), j * (self.room_size-1)),
                    (self.room_size, self.room_size)
                )
                room.doors = [[None]*self.doors_per_side]*4
                row.append(room)
                # Generate the walls for this room
                self.grid.wall_rect(*room.top, *room.size)

            self.room_grid.append(row)
        # For each row of rooms
        # import pdb; pdb.set_trace()
        for j in range(0, self.num_rows):
            # For each column of rooms
            for i in range(0, self.num_cols):
                room = self.room_grid[j][i]

                x_l, y_l = (room.top[0] + 1, room.top[1] + 1)
                x_m, y_m = (room.top[0] + room.size[0] - 1, room.top[1] + room.size[1] - 1)
                x_piece = (x_m-x_l)//self.doors_per_side
                y_piece = (y_m-y_l)//self.doors_per_side
                # Door positions, order is right, down, left, up
                if i <= self.num_cols - 1:
                    if i!=self.num_cols-1:
                        room.neighbors[0] = self.room_grid[j][i+1]
                    room.door_pos[0]=[]
                    # import pdb; pdb.set_trace()
                    for door_pos in self.door_pos_lst[j][i][0]:
                        room.door_pos[0].append((x_m, y_l+(door_pos*y_piece)))
                    if i==0:
                        # room.neighbors[2] = self.room_grid[j][i-1]
                        room.door_pos[2]=[]
                        for door_pos in self.door_pos_lst[j][i][2]:
                            room.door_pos[2].append((x_l-1, y_l+(door_pos*y_piece)))
                if j <= self.num_rows - 1:
                    if j!=self.num_rows-1:
                        room.neighbors[1] = self.room_grid[j+1][i]
                    room.door_pos[1]=[]
                    for door_pos in self.door_pos_lst[j][i][1]:
                        room.door_pos[1].append((x_l+(door_pos*x_piece), y_m))
                    if j==0:
                        # room.neighbors[3] = self.room_grid[j-1][i]
                        room.door_pos[3]=[]
                        for door_pos in self.door_pos_lst[j][i][3]:
                            room.door_pos[3].append((x_l+(door_pos*x_piece), y_l-1))
                if i > 0 and self.room_grid[j][i-1]:
                    room.neighbors[2] = self.room_grid[j][i-1]
                    room.door_pos[2] = room.neighbors[2].door_pos[0]
                # if not self.room_grid[j][i-1]:
                #     room.neighbors[2] = self.room_grid[j][i-1]
                #     room.door_pos[2]=[]
                #     for door_pos in self.door_pos_lst[2]:
                        # room.door_pos[2].append((x_m, y_l+(door_pos*y_piece)))
                if j > 0 and self.room_grid[j-1][i]:
                    room.neighbors[3] = self.room_grid[j-1][i]
                    room.door_pos[3] = room.neighbors[3].door_pos[1]
                # if not self.room_grid[j-1][i]:
                #     room.neighbors[3] = self.room_grid[j-1][i]
                #     room.door_pos[3]=[]
                #     for door_pos in self.door_pos_lst[3]:
                #         room.door_pos[3].append((x_l+(door_pos*x_piece), y_m))
        # The agent starts in the middle, facing right
        self.agent_pos = (
            (self.num_cols // 2) * (self.room_size-1) + (self.room_size // 2),
            (self.num_rows // 2) * (self.room_size-1) + (self.room_size // 2)
        )
        self.agent_dir = 0
        self.gen_mission()

        # Validate the instructions
        self.validate_instrs(self.instrs)


    def set_door_loc(self, door_idx, door_pos_lst):
        room.door_pos[door_idx]=[]
        for door_pos in door_pos_lst:
            room.door_pos[door_idx].append((x_m, y_l+door_pos))
                # if door_idx==0:
                    #room.neighbors[0] = self.room_grid[j][i+1]
                #     room.door_pos[door_idx]=[]
                #     for door_pos in door_pos_lst:
                #         room.door_pos[door_idx].append((x_m, y_l+door_pos))
                # if door_idx==1:
                #     #room.neighbors[1] = self.room_grid[j+1][i]
                #     room.door_pos[1] = (x_l +door_pos, y_m)
                #
                # if door_idx==2:
                #     #room.neighbors[2] = self.room_grid[j][i-1]
                #     room.door_pos[2] = room.neighbors[2].door_pos[0]
                # if door_idx==3:
                #     #room.neighbors[3] = self.room_grid[j-1][i]
                #     room.door_pos[3] = room.neighbors[3].door_pos[1]
#set door pos will be called first with predetermined number of doors and then add door will be called with the number of door given in set door pos paramter
    def add_door(self, i, j, door_idx=None, color=None, locked=None, doorid_on_idx=None):
        """
        Add a door to a room, connecting it to a neighbor
        """

        room = self.get_room(i, j)
        # print('BOOGIE WOOGIE')

        if door_idx == None:
            # Need to make sure that there is a neighbor along this wall
            # and that there is not already a door
            while True:
                door_idx = self._rand_int(0, 4)
                if room.neighbors[door_idx] and room.doors[door_idx][doorid_on_idx] is None:
                    break

        if color == None:
            color = self._rand_color()

        if locked is None:
            locked = self._rand_bool()

        assert room.doors[door_idx][doorid_on_idx] is None, "door already exists"
        room.locked = locked
        door = Door(color, is_locked=locked)
        #print('Door Index: ', door_idx)
        pos = room.door_pos[door_idx][doorid_on_idx]
        #print('Door Position: ', door_idx)

        self.grid.set(*pos, door)
        door.cur_pos = pos

        neighbor = room.neighbors[door_idx]
        room.doors[door_idx].append(door)
        if neighbor:
            neighbor.doors[(door_idx+2) % 4] = door

        return door, pos


    def add_object(self, i, j, kind=None, color=None, goalidx=None):
       """
       Add a new object to room (i, j)
       """

       if kind == None:
           kind = self._rand_elem(['key', 'ball', 'box'])

       if color == None:
           color = self._rand_color()

       # TODO: we probably want to add an Object.make helper function
       assert kind in ['key', 'ball', 'box', 'goal', 'goalcolor']
       if kind == 'key':
           obj = Key(color)
       elif kind == 'ball':
           obj = Ball(color)
       elif kind == 'box':
           obj = Box(color)
       elif kind == 'goal':
           obj: Goal()
       elif kind =='goalcolor':
           obj = GoalColor(color)
           #(0,0) means at center of room
           return self.put_obj(GoalColor(color), (((self.width - 1)//self.num_cols)*(i+1))-(2+goalidx[0]) , (((self.height-1)//self.num_rows)*(j+1))- (2+goalidx[1]))

       return self.place_in_room(i, j, obj)

    def reset(self, **kwargs):
        obs = super().reset(**kwargs)

        # Recreate the verifier
        # self.instrs.reset_verifier(self)

        # Compute the time step limit based on the maze size and instructions
        # nav_time_room = self.room_size ** 2
        # nav_time_maze = nav_time_room * self.num_rows * self.num_cols
        # num_navs = self.num_navs_needed(self.instrs)
        # self.max_steps = num_navs * nav_time_maze
        self.max_steps= self.steps_limit
        return obs

    def step(self, action):
        ''' To Be used by HRL Vickery code so avoid any other dependency issues
        - returns obs in named Tuple
        - with room num agent is in'''
        import pdb; pdb.set_trace()
        obs, reward, done, info = super().step(action)
        if not done and reward == 0: 
            reward=-.005
        return obs, reward, done, info
        
    def _reward(self):
        """
        Compute the reward to be given upon success
        """
        return 1 

    def gen_mission(self):
        # import pdb; pdb.set_trace()
        # start_room = 0
        # end_room = 2
        # rightwalldoors=[0,9]
        #self.set_door_loc(0, rightwalldoors)
        for r in range(0, self.num_rows):
            # For each column of rooms
            for c in range(0, self.num_cols):
                room_door_pos_lst = self.door_pos_lst[r][c]
                room_door_color_lst = self.door_color_lst[r][c]
                room_door_lock_lst = self.door_lock_lst[r][c]
                for i in range(len(room_door_pos_lst)):
                    for j in range(len(room_door_pos_lst[i])):
                        # print(room_door_color_lst[i][j]) 
                        # import pdb; pdb.set_trace()
                        obj, _ = self.add_door(c, r,i,  room_door_color_lst[i][j], locked=room_door_lock_lst[i][j], doorid_on_idx=j)
                for idx,obj in enumerate(self.room_objects[r][c]):
                    self.add_object(c, r, kind=obj[0], color=self.room_objects_color[r][c][idx], goalidx=obj[1])
        self.place_agent(self.start_room[1],self.start_room[0])
        # self.instrs = OpenInstr(ObjDesc('door', 'green'), room=end_room)
        # self.instrs = GoToGoalInstr(ObjDesc('box', 'green'))#, room=end_room)

######NEED TO FIX: CANT MAKE DOORS AFTER IDX 1 for Dooridxs in [0,1,2,3]

def setup_doors(doors, rows, cols):
    door_pos_lst = [[[[] for i in range(4)] for j in range(cols)] for k in range(rows)]
    door_color_lst = [[[[] for i in range(4)] for j in range(cols)] for k in range(rows)]
    door_lock_lst = [[[[] for i in range(4)] for j in range(cols)] for k in range(rows)]

    for id in doors/keys(): 
        door_pos_lst[doors[id].row][doors[id].col][doors[id].wall] = doors[id].index
        door_color_lst[doors[id].row][doors[id].col][doors[id].wall] = doors[id].color
        door_lock_lst[doors[id].row][doors[id].col][doors[id].wall] = doors[id].lock
    return door_pos_lst, door_color_lst, door_lock_lst

#Example Use :
        # doors = {0: DoorInfo(row=, col=, wall=, index=, color=, lock=)}


class DoorInfo():
    def __init__(self, row, col, wall, index, color , lock):
        self.row = row
        self.col = col
        self.wall = wall 
        self.index =index
        self.color= color 
        self.lock = lock


class Level_ProofABCEDPretrainTest(ProofTest):
    """
    Subtask A in transfer learning env setup
    """

    def __init__(self, seed=None, doors_per_side=3):
        # doors = {0: Door (row=, col=, wall=, index=, color=, lock=)}
        args = {'door_pos_lst': [[[[1], [], [], []],   [[1], [], [], []],   [[0,2], [], [], []], [[], [], [], []]]],
                'door_color_lst':  [[[['yellow'], [], [], []],   [['purple'], [], [], []],   [['red', 'blue'], [], [], []], [[], [], [], []]]],
                'door_lock_lst': [[[[False], [], [], []],   [[False], [], [], []],   [[False,False], [], [], []], [[], [], [], []]]],
                'room_objects': [[[],[],[],[['goalcolor',(-1,0)]]]],
                'room_objects_color': [[[], [], [], ['green']]],
                'width': None,
                'height': None}
        super().__init__(
            start_room = [0,0],
            instrs = GoToGoalInstr(ObjDesc('box', 'green')),#, room=end_room),
            args=args,
            steps_limit=100,
            step_reward=-0.005)

class Level_ProofABEDTransferTest(ProofTest):
    """
    Subtask A in transfer learning env setup
    """

    def __init__(self, seed=None, doors_per_side=3):
        # doors = {0: Door (row=, col=, wall=, index=, color=, lock=)}
        args = {'door_pos_lst': [[[[1], [], [], []],   [[1], [], [], []],   [[0,2], [], [], []], [[], [], [], []]]],
                'door_color_lst':  [[[['yellow'], [], [], []],   [['purple'], [], [], []],   [['red', 'blue'], [], [], []], [[], [], [], []]]],
                'door_lock_lst': [[[[False], [], [], []],   [[False], [], [], []],   [[True,False], [], [], []], [[], [], [], []]]],
                'room_objects': [[[],[],[],[['goalcolor',(-1,0)]]]],
                'room_objects_color': [[[], [], [], ['green']]],
                'width': None,
                'height': None}
        super().__init__(
            start_room = [0,0],
            instrs = GoToGoalInstr(ObjDesc('box', 'green')),#, room=end_room),
            args=args,
            steps_limit=100,
            step_reward=-0.005)

class Level_ProofABPrimTest(ProofTest):
    """
    Subtask A in transfer learning env setup
    """

    def __init__(self, seed=None, doors_per_side=3):
        # doors = {0: Door (row=, col=, wall=, index=, color=, lock=)}
        args = {'door_pos_lst': [[[[1], [], [], []],   [[1], [], [], []],   [[0,2], [], [], []], [[], [], [], []]]],
                'door_color_lst':  [[[['yellow'], [], [], []],   [['purple'], [], [], []],   [['red', 'blue'], [], [], []], [[], [], [], []]]],
                'door_lock_lst': [[[[False], [], [], []],   [[False], [], [], []],   [[True,True], [], [], []], [[], [], [], []]]],
                'room_objects': [[[],[],[],[['goalcolor',(-1,0)]]]],
                'room_objects_color': [[[], [], [], ['green']]],
                'width': None,
                'height': None}
        super().__init__(
            start_room = [0,0],
            instrs =  OpenInstrTwoRoom(ObjDesc('door', 'purple'), room=[0,2]),
            args=args,
            steps_limit=100,
            step_reward=-0.005)


class Level_ProofAPrimTest(ProofTest):
    """
    Subtask A in transfer learning env setup
    """

    def __init__(self, seed=None, doors_per_side=3):
        # doors = {0: Door (row=, col=, wall=, index=, color=, lock=)}
        args = {'door_pos_lst': [[[[1], [], [], []],   [[1], [], [], []],   [[0,2], [], [], []], [[], [], [], []]]],
                'door_color_lst':  [[[['yellow'], [], [], []],   [['purple'], [], [], []],   [['red', 'blue'], [], [], []], [[], [], [], []]]],
                'door_lock_lst': [[[[False], [], [], []],   [[False], [], [], []],   [[False,False], [], [], []], [[], [], [], []]]],
                'room_objects': [[[],[],[],[['goalcolor',(-1,0)]]]],
                'room_objects_color': [[[], [], [], ['green']]],
                'width': None,
                'height': None}
        super().__init__(
            start_room = [0,0],
            instrs =  OpenInstrTwoRoom(ObjDesc('door', 'yellow'), room=[0,1]),
            args=args,
            steps_limit=100,
            step_reward=-0.005)

class Level_ProofBPrimTest(ProofTest):
    """
    Subtask A in transfer learning env setup
    """

    def __init__(self, seed=None, doors_per_side=3):
        # doors = {0: Door (row=, col=, wall=, index=, color=, lock=)}
        args = {'door_pos_lst': [[[[1], [], [], []],   [[1], [], [], []],   [[0,2], [], [], []], [[], [], [], []]]],
                'door_color_lst':  [[[['yellow'], [], [], []],   [['purple'], [], [], []],   [['red', 'blue'], [], [], []], [[], [], [], []]]],
                'door_lock_lst': [[[[False], [], [], []],   [[False], [], [], []],   [[False,False], [], [], []], [[], [], [], []]]],
                'room_objects': [[[],[],[],[['goalcolor',(-1,0)]]]],
                'room_objects_color': [[[], [], [], ['green']]],
                'width': None,
                'height': None}
        super().__init__(
            start_room = [0,1],
            instrs =  OpenInstrTwoRoom(ObjDesc('door', 'purple'), room=[0,2]),
            args=args,
            steps_limit=100,
            step_reward=-0.005)

class Level_ProofCPrimTest(ProofTest):
    """
    Subtask A in transfer learning env setup
    """

    def __init__(self, seed=None, doors_per_side=3):
        # doors = {0: Door (row=, col=, wall=, index=, color=, lock=)}
        args = {'door_pos_lst': [[[[1], [], [], []],   [[1], [], [], []],   [[0,2], [], [], []], [[], [], [], []]]],
                'door_color_lst':  [[[['yellow'], [], [], []],   [['purple'], [], [], []],   [['red', 'blue'], [], [], []], [[], [], [], []]]],
                'door_lock_lst': [[[[False], [], [], []],   [[False], [], [], []],   [[False,False], [], [], []], [[], [], [], []]]],
                'room_objects': [[[],[],[],[['goalcolor',(-1,0)]]]],
                'room_objects_color': [[[], [], [], ['green']]],
                'width': None,
                'height': None}
        super().__init__(
            start_room = [0,2],
            instrs =  OpenInstrTwoRoom(ObjDesc('door', 'red'), room=[0,3]),
            args=args,
            steps_limit=100,
            step_reward=-0.005)

class Level_ProofEPrimTest(ProofTest):
    """
    Subtask A in transfer learning env setup
    """

    def __init__(self, seed=None, doors_per_side=3):
        # doors = {0: Door (row=, col=, wall=, index=, color=, lock=)}
        args = {'door_pos_lst': [[[[1], [], [], []],   [[1], [], [], []],   [[0,2], [], [], []], [[], [], [], []]]],
                'door_color_lst':  [[[['yellow'], [], [], []],   [['purple'], [], [], []],   [['red', 'blue'], [], [], []], [[], [], [], []]]],
                'door_lock_lst': [[[[False], [], [], []],   [[False], [], [], []],   [[False,False], [], [], []], [[], [], [], []]]],
                'room_objects': [[[],[],[],[['goalcolor',(-1,0)]]]],
                'room_objects_color': [[[], [], [], ['green']]],
                'width': None,
                'height': None}
        super().__init__(
            start_room = [0,2],
            instrs =  OpenInstrTwoRoom(ObjDesc('door', 'blue'), room=[0,3]),
            args=args,
            steps_limit=100,
            step_reward=-0.005)

class Level_ProofDPrimTest(ProofTest):
    """
    Subtask A in transfer learning env setup
    """

    def __init__(self, seed=None, doors_per_side=3):
        # doors = {0: Door (row=, col=, wall=, index=, color=, lock=)}
        args = {'door_pos_lst': [[[[1], [], [], []],   [[1], [], [], []],   [[0,2], [], [], []], [[], [], [], []]]],
                'door_color_lst':  [[[['yellow'], [], [], []],   [['purple'], [], [], []],   [['red', 'blue'], [], [], []], [[], [], [], []]]],
                'door_lock_lst': [[[[False], [], [], []],   [[False], [], [], []],   [[False,False], [], [], []], [[], [], [], []]]],
                'room_objects': [[[],[],[],[['goalcolor',(-1,0)]]]],
                'room_objects_color': [[[], [], [], ['green']]],
                'width': None,
                'height': None}
        super().__init__(
            start_room = [0,3],
            instrs = GoToGoalInstr(ObjDesc('box', 'green')),#, room=end_room),
            args=args,
            steps_limit=100,
            step_reward=-0.005)

    
class Level_LinearChainPretrainABCTest(ProofTest):
    """
    Subtask A in transfer learning env setup
    """

    def __init__(self, seed=None, doors_per_side=3):
        # doors = {0: Door (row=, col=, wall=, index=, color=, lock=)}
        args = {'door_pos_lst': [[[[0,2], [], [], []],   [[0,2], [], [], []],   [[0,2], [], [], []], [[], [], [], []]]],
                'door_color_lst':  [[[['yellow', 'green'], [], [], []],   [['purple', 'grey'], [], [], []],   [['red', 'blue'], [], [], []], [[], [], [], []]]],
                'door_lock_lst': [[[[False, True], [], [], []],   [[False, True], [], [], []],   [[False,True], [], [], []], [[], [], [], []]]],
                'room_objects': [[[],[],[],[]]],
                'room_objects_color': [[[], [], [], []]],
                'width': None,
                'height': None}
        super().__init__(
            start_room = [0,0],
            instrs =  OpenInstrTwoRoom(ObjDesc('door', 'red'), room=[0,3]),
            args=args,
            steps_limit=100,
            step_reward=-0.005)

class Level_LinearChainTransferABDTest(ProofTest):
    """
    Subtask A in transfer learning env setup
    """

    def __init__(self, seed=None, doors_per_side=3):
        # doors = {0: Door (row=, col=, wall=, index=, color=, lock=)}
        args = {'door_pos_lst': [[[[0,2], [], [], []],   [[0,2], [], [], []],   [[0,2], [], [], []], [[], [], [], []]]],
                'door_color_lst':  [[[['yellow', 'green'], [], [], []],   [['purple', 'grey'], [], [], []],   [['red', 'blue'], [], [], []], [[], [], [], []]]],
                'door_lock_lst': [[[[False, True], [], [], []],   [[False, True], [], [], []],   [[True, False], [], [], []], [[], [], [], []]]],
                'room_objects': [[[],[],[],[]]],
                'room_objects_color': [[[], [], [], []]],
                'width': None,
                'height': None}
        super().__init__(
            start_room = [0,0],
            instrs =  OpenInstrTwoRoom(ObjDesc('door', 'blue'), room=[0,3]),
            args=args,
            steps_limit=100,
            step_reward=-0.005)

class Level_LinearChainTransferAECTest(ProofTest):
    """
    Subtask A in transfer learning env setup
    """

    def __init__(self, seed=None, doors_per_side=3):
        # doors = {0: Door (row=, col=, wall=, index=, color=, lock=)}
        args = {'door_pos_lst': [[[[0,2], [], [], []],   [[0,2], [], [], []],   [[0,2], [], [], []], [[], [], [], []]]],
                'door_color_lst':  [[[['yellow', 'green'], [], [], []],   [['purple', 'grey'], [], [], []],   [['red', 'blue'], [], [], []], [[], [], [], []]]],
                'door_lock_lst': [[[[False, True], [], [], []],   [[True, False], [], [], []],   [[False,True], [], [], []], [[], [], [], []]]],
                'room_objects': [[[],[],[],[]]],
                'room_objects_color': [[[], [], [], []]],
                'width': None,
                'height': None}
        super().__init__(
            start_room = [0,0],
            instrs =  OpenInstrTwoRoom(ObjDesc('door', 'red'), room=[0,3]),
            args=args,
            steps_limit=100,
            step_reward=-0.005)

class Level_LinearChainTransferFBCTest(ProofTest):
    """
    Subtask A in transfer learning env setup
    """

    def __init__(self, seed=None, doors_per_side=3):
        # doors = {0: Door (row=, col=, wall=, index=, color=, lock=)}
        args = {'door_pos_lst': [[[[0,2], [], [], []],   [[0,2], [], [], []],   [[0,2], [], [], []], [[], [], [], []]]],
                'door_color_lst':  [[[['yellow', 'green'], [], [], []],   [['purple', 'grey'], [], [], []],   [['red', 'blue'], [], [], []], [[], [], [], []]]],
                'door_lock_lst': [[[[True, False], [], [], []],   [[False, True], [], [], []],   [[False,True], [], [], []], [[], [], [], []]]],
                'room_objects': [[[],[],[],[]]],
                'room_objects_color': [[[], [], [], []]],
                'width': None,
                'height': None}
        super().__init__(
            start_room = [0,0],
            instrs =  OpenInstrTwoRoom(ObjDesc('door', 'red'), room=[0,3]),
            args=args,
            steps_limit=100,
            step_reward=-0.005)


class Level_LinearChainAPrimTest(ProofTest):
    """
    Subtask A in transfer learning env setup
    """

    def __init__(self, seed=None, doors_per_side=3):
        # doors = {0: Door (row=, col=, wall=, index=, color=, lock=)}
        args = {'door_pos_lst': [[[[0,2], [], [], []],   [[0,2], [], [], []],   [[0,2], [], [], []], [[], [], [], []]]],
                'door_color_lst':  [[[['yellow', 'green'], [], [], []],   [['purple', 'grey'], [], [], []],   [['red', 'blue'], [], [], []], [[], [], [], []]]],
                'door_lock_lst': [[[[False, True], [], [], []],   [[True, True], [], [], []],   [[True,True], [], [], []], [[], [], [], []]]],
                'room_objects': [[[],[],[],[]]],
                'room_objects_color': [[[], [], [], []]],
                'width': None,
                'height': None}
        super().__init__(
            start_room = [0,0],
            instrs =  OpenInstrTwoRoom(ObjDesc('door', 'yellow'), room=[0,1]),
            args=args,
            steps_limit=50,
            step_reward=-0.005)

class Level_LinearChainBPrimTest(ProofTest):
    """
    Subtask A in transfer learning env setup
    """

    def __init__(self, seed=None, doors_per_side=3):
        # doors = {0: Door (row=, col=, wall=, index=, color=, lock=)}
        args = {'door_pos_lst': [[[[0,2], [], [], []],   [[0,2], [], [], []],   [[0,2], [], [], []], [[], [], [], []]]],
                'door_color_lst':  [[[['yellow', 'green'], [], [], []],   [['purple', 'grey'], [], [], []],   [['red', 'blue'], [], [], []], [[], [], [], []]]],
                'door_lock_lst': [[[[True, False], [], [], []],   [[True, True], [], [], []],   [[True,True], [], [], []], [[], [], [], []]]],
                'room_objects': [[[],[],[],[]]],
                'room_objects_color': [[[], [], [], []]],
                'width': None,
                'height': None}
        super().__init__(
            start_room = [0,0],
            instrs =  OpenInstrTwoRoom(ObjDesc('door', 'green'), room=[0,1]),
            args=args,
            steps_limit=50,
            step_reward=-0.005)

class Level_LinearChainCPrimTest(ProofTest):
    """
    Subtask A in transfer learning env setup
    """

    def __init__(self, seed=None, doors_per_side=3):
        # doors = {0: Door (row=, col=, wall=, index=, color=, lock=)}
        args = {'door_pos_lst': [[[[0,2], [], [], []],   [[0,2], [], [], []],   [[0,2], [], [], []], [[], [], [], []]]],
                'door_color_lst':  [[[['yellow', 'green'], [], [], []],   [['purple', 'grey'], [], [], []],   [['red', 'blue'], [], [], []], [[], [], [], []]]],
                'door_lock_lst': [[[[True, True], [], [], []],   [[False, True], [], [], []],   [[True,True], [], [], []], [[], [], [], []]]],
                'room_objects': [[[],[],[],[]]],
                'room_objects_color': [[[], [], [], []]],
                'width': None,
                'height': None}
        super().__init__(
            start_room = [0,1],
            instrs =  OpenInstrTwoRoom(ObjDesc('door', 'purple'), room=[0,2]),
            args=args,
            steps_limit=50,
            step_reward=-0.005)

class Level_LinearChainDPrimTest(ProofTest):
    """
    Subtask A in transfer learning env setup
    """

    def __init__(self, seed=None, doors_per_side=3):
        # doors = {0: Door (row=, col=, wall=, index=, color=, lock=)}
        args = {'door_pos_lst': [[[[0,2], [], [], []],   [[0,2], [], [], []],   [[0,2], [], [], []], [[], [], [], []]]],
                'door_color_lst':  [[[['yellow', 'green'], [], [], []],   [['purple', 'grey'], [], [], []],   [['red', 'blue'], [], [], []], [[], [], [], []]]],
                'door_lock_lst': [[[[True, True], [], [], []],   [[True, False], [], [], []],   [[True,True], [], [], []], [[], [], [], []]]],
                'room_objects': [[[],[],[],[]]],
                'room_objects_color': [[[], [], [], []]],
                'width': None,
                'height': None}
        super().__init__(
            start_room = [0,1],
            instrs =  OpenInstrTwoRoom(ObjDesc('door', 'grey'), room=[0,2]),
            args=args,
            steps_limit=50,
            step_reward=-0.005)

class Level_LinearChainEPrimTest(ProofTest):
    """
    Subtask A in transfer learning env setup
    """

    def __init__(self, seed=None, doors_per_side=3):
        # doors = {0: Door (row=, col=, wall=, index=, color=, lock=)}
        args = {'door_pos_lst': [[[[0,2], [], [], []],   [[0,2], [], [], []],   [[0,2], [], [], []], [[], [], [], []]]],
                'door_color_lst':  [[[['yellow', 'green'], [], [], []],   [['purple', 'grey'], [], [], []],   [['red', 'blue'], [], [], []], [[], [], [], []]]],
                'door_lock_lst': [[[[True, True], [], [], []],   [[True, True], [], [], []],   [[False,True], [], [], []], [[], [], [], []]]],
                'room_objects': [[[],[],[],[]]],
                'room_objects_color': [[[], [], [], []]],
                'width': None,
                'height': None}
        super().__init__(
            start_room = [0,2],
            instrs =  OpenInstrTwoRoom(ObjDesc('door', 'red'), room=[0,3]),
            args=args,
            steps_limit=50,
            step_reward=-0.005)

class Level_LinearChainFPrimTest(ProofTest):
    """
    Subtask A in transfer learning env setup
    """

    def __init__(self, seed=None, doors_per_side=3):
        # doors = {0: Door (row=, col=, wall=, index=, color=, lock=)}
        args = {'door_pos_lst': [[[[0,2], [], [], []],   [[0,2], [], [], []],   [[0,2], [], [], []], [[], [], [], []]]],
                'door_color_lst':  [[[['yellow', 'green'], [], [], []],   [['purple', 'grey'], [], [], []],   [['red', 'blue'], [], [], []], [[], [], [], []]]],
                'door_lock_lst': [[[[True, True], [], [], []],   [[True, True], [], [], []],   [[True,False], [], [], []], [[], [], [], []]]],
                'room_objects': [[[],[],[],[]]],
                'room_objects_color': [[[], [], [], []]],
                'width': None,
                'height': None}
        super().__init__(
            start_room = [0,2],
            instrs =  OpenInstrTwoRoom(ObjDesc('door', 'blue'), room=[0,3]),
            args=args,
            steps_limit=50,
            step_reward=-0.005)

# class Level_InvarPrimBTest(InvarianceTest):
#     """
#     Subtask A in transfer learning env setup
#     """

#     def __init__(self, seed=None, doors_per_side=3):
#         args = {'door_pos_lst': [[[[], [], [], []],   [[], [1], [], []],   [[],[],[],[]]], [[[1], [], [], []],   [[1], [1], [], []],   [[],[],[],[]]], [[[], [], [], []],   [[], [], [], []],   [[],[],[],[]]]],
#                 'door_color_lst':  [[[[], [], [], []], [[], ['yellow'], [], []], [[], [], [], []]], [[['red'], [], [], []], [['green'], ['blue'], [], []], [[], [], [], []]], [[[], [], [], []], [[], [], [], []], [[], [], [], []]]],
#                 'door_lock_lst': [[[[], [], [], []], [[], [False], [], []], [[], [], [], []]], [[[False], [], [], []], [[False], [False], [], []], [[], [], [], []]], [[[], [], [], []], [[], [], [], []], [[], [], [], []]]],
#                 'room_objects': [[[],[],[]], [[],[],[['goalcolor',(-1,0)]]], [[],[['goalcolor',(0,-1)]],[]]],
#                 'room_objects_color': [[[], [], []], [[], [], ['green']], [[], ['blue'], []]],
#                 'width': None,
#                 'height': None}
#         super().__init__(
#             start_room = [1,0],
#             instrs =  OpenInstrTwoRoom(ObjDesc('door', 'yellow'), room=[1,1]),
#             args=args,
#             steps_limit=50)

# class Level_InvarPrimCTest(InvarianceTest):
#     """
#     Subtask A in transfer learning env setup
#     """

#     def __init__(self, seed=None, doors_per_side=3):
#         args = {'door_pos_lst': [[[[], [], [], []],   [[], [1], [], []],   [[],[],[],[]]], [[[1], [], [], []],   [[1], [1], [], []],   [[],[],[],[]]], [[[], [], [], []],   [[], [], [], []],   [[],[],[],[]]]],
#                 'door_color_lst':  [[[[], [], [], []], [[], ['yellow'], [], []], [[], [], [], []]], [[['red'], [], [], []], [['green'], ['blue'], [], []], [[], [], [], []]], [[[], [], [], []], [[], [], [], []], [[], [], [], []]]],
#                 'door_lock_lst': [[[[], [], [], []], [[], [False], [], []], [[], [], [], []]], [[[False], [], [], []], [[False], [False], [], []], [[], [], [], []]], [[[], [], [], []], [[], [], [], []], [[], [], [], []]]],
#                 'room_objects': [[[],[],[]], [[],[],[['goalcolor',(-1,0)]]], [[],[['goalcolor',(0,-1)]],[]]],
#                 'room_objects_color': [[[], [], []], [[], [], ['green']], [[], ['blue'], []]],
#                 'width': None,
#                 'height': None}
#         super().__init__(
#             start_room = [1,1],
#             instrs = GoToGoalInstr(ObjDesc('box', 'blue')),#, room=end_room),
#             args=args,
#             steps_limit=50)

# class Level_InvarPrimCKeyTest(InvarianceTest):
#     """
#     Subtask A in transfer learning env setup
#     """

#     def __init__(self, seed=None, doors_per_side=3):
#         args = {'door_pos_lst': [[[[], [], [], []],   [[], [1], [], []],   [[],[],[],[]]], [[[1], [], [], []],   [[1], [1], [], []],   [[],[],[],[]]], [[[], [], [], []],   [[], [], [], []],   [[],[],[],[]]]],
#                 'door_color_lst':  [[[[], [], [], []], [[], ['yellow'], [], []], [[], [], [], []]], [[['red'], [], [], []], [['green'], ['blue'], [], []], [[], [], [], []]], [[[], [], [], []], [[], [], [], []], [[], [], [], []]]],
#                 'door_lock_lst': [[[[], [], [], []], [[], [False], [], []], [[], [], [], []]], [[[False], [], [], []], [[True], [True], [], []], [[], [], [], []]], [[[], [], [], []], [[], [], [], []], [[], [], [], []]]],
#                 'room_objects': [[[],[],[]], [[],[['key', 0]],[]], [[],[],[]]],
#                 'room_objects_color': [[[], [], []], [[], ['blue'], []], [[], [], []]],
#                 'width': None,
#                 'height': None}
#         super().__init__(
#             start_room = [1,1],
#             instrs =  OpenInstrTwoRoom(ObjDesc('door', 'blue'), room=[2,1]),
#             args=args,
#             steps_limit=50)

# class Level_InvarPrimDKeyTest(InvarianceTest):
#     """
#     Subtask A in transfer learning env setup
#     """

#     def __init__(self, seed=None, doors_per_side=3):
#         args = {'door_pos_lst': [[[[], [], [], []],   [[], [1], [], []],   [[],[],[],[]]], [[[1], [], [], []],   [[1], [1], [], []],   [[],[],[],[]]], [[[], [], [], []],   [[], [], [], []],   [[],[],[],[]]]],
#                 'door_color_lst':  [[[[], [], [], []], [[], ['yellow'], [], []], [[], [], [], []]], [[['red'], [], [], []], [['green'], ['blue'], [], []], [[], [], [], []]], [[[], [], [], []], [[], [], [], []], [[], [], [], []]]],
#                 'door_lock_lst': [[[[], [], [], []], [[], [False], [], []], [[], [], [], []]], [[[False], [], [], []], [[True], [True], [], []], [[], [], [], []]], [[[], [], [], []], [[], [], [], []], [[], [], [], []]]],
#                 'room_objects': [[[],[],[]], [[],[['key', 0]],[]], [[],[],[]]],
#                 'room_objects_color': [[[], [], []], [[], ['green'], []], [[], [], []]],
#                 'width': None,
#                 'height': None}
#         super().__init__(
#             start_room = [1,1],
#             instrs =  OpenInstrTwoRoom(ObjDesc('door', 'green'), room=[1,2]),
#             args=args,
#             steps_limit=50)

# class Level_InvarPrimDTest(InvarianceTest):
#     """
#     Subtask A in transfer learning env setup
#     """

#     def __init__(self, seed=None, doors_per_side=3):
#         args = {'door_pos_lst': [[[[], [], [], []],   [[], [1], [], []],   [[],[],[],[]]], [[[1], [], [], []],   [[1], [1], [], []],   [[],[],[],[]]], [[[], [], [], []],   [[], [], [], []],   [[],[],[],[]]]],
#                 'door_color_lst':  [[[[], [], [], []], [[], ['yellow'], [], []], [[], [], [], []]], [[['red'], [], [], []], [['green'], ['blue'], [], []], [[], [], [], []]], [[[], [], [], []], [[], [], [], []], [[], [], [], []]]],
#                 'door_lock_lst': [[[[], [], [], []], [[], [False], [], []], [[], [], [], []]], [[[False], [], [], []], [[False], [False], [], []], [[], [], [], []]], [[[], [], [], []], [[], [], [], []], [[], [], [], []]]],
#                 'room_objects': [[[],[],[]], [[],[],[['goalcolor',(-1,0)]]], [[],[['goalcolor',(0,-1)]],[]]],
#                 'room_objects_color': [[[], [], []], [[], [], ['green']], [[], ['blue'], []]],
#                 'width': None,
#                 'height': None}
#         super().__init__(
#             start_room = [1,1],
#             instrs = GoToGoalInstr(ObjDesc('box', 'green')),#, room=end_room),
#             args=args,
#             steps_limit=50)

# class Level_Invar1Test(InvarianceTest):
#     """
#     Subtask A in transfer learning env setup
#     """

#     def __init__(self, seed=None, doors_per_side=3):
#         args = {'door_pos_lst': [[[[], [], [], []],   [[], [1], [], []],   [[],[],[],[]]], [[[1], [], [], []],   [[1], [1], [], []],   [[],[],[],[]]], [[[], [], [], []],   [[], [], [], []],   [[],[],[],[]]]],
#                 'door_color_lst':  [[[[], [], [], []], [[], ['yellow'], [], []], [[], [], [], []]], [[['red'], [], [], []], [['green'], ['blue'], [], []], [[], [], [], []]], [[[], [], [], []], [[], [], [], []], [[], [], [], []]]],
#                 'door_lock_lst': [[[[], [], [], []], [[], [False], [], []], [[], [], [], []]], [[[False], [], [], []], [[False], [False], [], []], [[], [], [], []]], [[[], [], [], []], [[], [], [], []], [[], [], [], []]]],
#                 'room_objects': [[[],[],[]], [[],[],[['goalcolor',(-1,0)]]], [[],[['goalcolor',(0,-1)]],[]]],
#                 'room_objects_color': [[[], [], []], [[], [], ['green']], [[], ['blue'], []]],
#                 'width': None,
#                 'height': None}
#         super().__init__(
#             start_room = [0,1],
#             instrs = GoToGoalInstr(ObjDesc('box', 'blue')),#, room=end_room),
#             args=args,
#             steps_limit=50)

# class Level_Invar1KeyTest(InvarianceTest):
#     """
#     Subtask A in transfer learning env setup
#     """

#     def __init__(self, seed=None, doors_per_side=3):
#         args = {'door_pos_lst': [[[[], [], [], []],   [[], [1], [], []],   [[],[],[],[]]], [[[1], [], [], []],   [[1], [1], [], []],   [[],[],[],[]]], [[[], [], [], []],   [[], [], [], []],   [[],[],[],[]]]],
#                 'door_color_lst':  [[[[], [], [], []], [[], ['yellow'], [], []], [[], [], [], []]], [[['red'], [], [], []], [['green'], ['blue'], [], []], [[], [], [], []]], [[[], [], [], []], [[], [], [], []], [[], [], [], []]]],
#                 'door_lock_lst': [[[[], [], [], []], [[], [False], [], []], [[], [], [], []]], [[[False], [], [], []], [[False], [False], [], []], [[], [], [], []]], [[[], [], [], []], [[], [], [], []], [[], [], [], []]]],
#                 'room_objects': [[[],[],[]], [[],[['key', 0]],[]], [[],[],[]]],
#                 'room_objects_color': [[[], [], []], [[], ['blue'], []], [[], [], []]],
#                 'width': None,
#                 'height': None}
#         super().__init__(
#             start_room = [0,1],
#             instrs =  OpenInstrTwoRoom(ObjDesc('door', 'blue'), room=[2,1]),
#             args=args,
#             steps_limit=50)

# class Level_Invar2Test(InvarianceTest):
#     """
#     Subtask A in transfer learning env setup
#     """

#     def __init__(self, seed=None, doors_per_side=3):
#         args = {'door_pos_lst': [[[[], [], [], []],   [[], [1], [], []],   [[],[],[],[]]], [[[1], [], [], []],   [[1], [1], [], []],   [[],[],[],[]]], [[[], [], [], []],   [[], [], [], []],   [[],[],[],[]]]],
#                 'door_color_lst':  [[[[], [], [], []], [[], ['yellow'], [], []], [[], [], [], []]], [[['red'], [], [], []], [['green'], ['blue'], [], []], [[], [], [], []]], [[[], [], [], []], [[], [], [], []], [[], [], [], []]]],
#                 'door_lock_lst': [[[[], [], [], []], [[], [False], [], []], [[], [], [], []]], [[[False], [], [], []], [[False], [False], [], []], [[], [], [], []]], [[[], [], [], []], [[], [], [], []], [[], [], [], []]]],
#                 'room_objects': [[[],[],[]], [[],[],[['goalcolor',(-1,0)]]], [[],[['goalcolor',(0,-1)]],[]]],
#                 'room_objects_color': [[[], [], []], [[], [], ['green']], [[], ['blue'], []]],
#                 'width': None,
#                 'height': None}
#         super().__init__(
#             start_room = [1,0],
#             instrs = GoToGoalInstr(ObjDesc('box', 'green')),#, room=end_room),
#             args=args,
#             steps_limit=50)

# class Level_Invar2KeyTest(InvarianceTest):
#     """
#     Subtask A in transfer learning env setup
#     """

#     def __init__(self, seed=None, doors_per_side=3):
#         args = {'door_pos_lst': [[[[], [], [], []],   [[], [1], [], []],   [[],[],[],[]]], [[[1], [], [], []],   [[1], [1], [], []],   [[],[],[],[]]], [[[], [], [], []],   [[], [], [], []],   [[],[],[],[]]]],
#                 'door_color_lst':  [[[[], [], [], []], [[], ['yellow'], [], []], [[], [], [], []]], [[['red'], [], [], []], [['green'], ['blue'], [], []], [[], [], [], []]], [[[], [], [], []], [[], [], [], []], [[], [], [], []]]],
#                 'door_lock_lst': [[[[], [], [], []], [[], [False], [], []], [[], [], [], []]], [[[False], [], [], []], [[False], [False], [], []], [[], [], [], []]], [[[], [], [], []], [[], [], [], []], [[], [], [], []]]],
#                 'room_objects': [[[],[],[]], [[],[['key', 0]],[]], [[],[],[]]],
#                 'room_objects_color': [[[], [], []], [[], ['green'], []], [[], [], []]],
#                 'width': None,
#                 'height': None}
#         super().__init__(
#             start_room = [1,0],
#             instrs =  OpenInstrTwoRoom(ObjDesc('door', 'green'), room=[1,2]),
#             args=args,
#             steps_limit=50)

# class Level_Parallel1Test(InvarianceTest):
#     """
#     Subtask A in transfer learning env setup
#     """

#     def __init__(self, seed=None, doors_per_side=3):
#         args = {'door_pos_lst': [[[[], [], [], []],   [[], [1], [], []],   [[],[],[],[]]], [[[1], [], [], []],   [[1], [1], [], []],   [[],[],[],[]]], [[[], [], [], []],   [[], [], [], []],   [[],[],[],[]]]],
#                 'door_color_lst':  [[[[], [], [], []], [[], ['yellow'], [], []], [[], [], [], []]], [[['red'], [], [], []], [['green'], ['blue'], [], []], [[], [], [], []]], [[[], [], [], []], [[], [], [], []], [[], [], [], []]]],
#                 'door_lock_lst': [[[[], [], [], []], [[], [False], [], []], [[], [], [], []]], [[[False], [], [], []], [[False], [False], [], []], [[], [], [], []]], [[[], [], [], []], [[], [], [], []], [[], [], [], []]]],
#                 'room_objects': [[[],[],[]], [[],[],[['goalcolor',(-1,0)]]], [[],[['goalcolor',(0,-1)]],[]]],
#                 'room_objects_color': [[[], [], []], [[], [], ['green']], [[], ['blue'], []]],
#                 'width': None,
#                 'height': None}
#         super().__init__(
#             start_room = [0,1],
#             instrs = GoToGoalInstr(ObjDesc('box', 'green')),#, room=end_room),
#             args=args,
#             steps_limit=50)

# class Level_Parallel1KeyTest(InvarianceTest):
#     """
#     Subtask A in transfer learning env setup
#     """

#     def __init__(self, seed=None, doors_per_side=3):
#         args = {'door_pos_lst': [[[[], [], [], []],   [[], [1], [], []],   [[],[],[],[]]], [[[1], [], [], []],   [[1], [1], [], []],   [[],[],[],[]]], [[[], [], [], []],   [[], [], [], []],   [[],[],[],[]]]],
#                 'door_color_lst':  [[[[], [], [], []], [[], ['yellow'], [], []], [[], [], [], []]], [[['red'], [], [], []], [['green'], ['blue'], [], []], [[], [], [], []]], [[[], [], [], []], [[], [], [], []], [[], [], [], []]]],
#                 'door_lock_lst': [[[[], [], [], []], [[], [False], [], []], [[], [], [], []]], [[[False], [], [], []], [[False], [False], [], []], [[], [], [], []]], [[[], [], [], []], [[], [], [], []], [[], [], [], []]]],
#                 'room_objects': [[[],[],[]], [[],[['key', 0]],[]], [[],[],[]]],
#                 'room_objects_color': [[[], [], []], [[], ['green'], []], [[], [], []]],
#                 'width': None,
#                 'height': None}
#         super().__init__(
#             start_room = [0,1],
#             instrs =  OpenInstrTwoRoom(ObjDesc('door', 'green'), room=[1,2]),
#             args=args,
#             steps_limit=50)

# class Level_Parallel2Test(InvarianceTest):
#     """
#     Subtask A in transfer learning env setup
#     """

#     def __init__(self, seed=None, doors_per_side=3):
#         args = {'door_pos_lst': [[[[], [], [], []],   [[], [1], [], []],   [[],[],[],[]]], [[[1], [], [], []],   [[1], [1], [], []],   [[],[],[],[]]], [[[], [], [], []],   [[], [], [], []],   [[],[],[],[]]]],
#                 'door_color_lst':  [[[[], [], [], []], [[], ['yellow'], [], []], [[], [], [], []]], [[['red'], [], [], []], [['green'], ['blue'], [], []], [[], [], [], []]], [[[], [], [], []], [[], [], [], []], [[], [], [], []]]],
#                 'door_lock_lst': [[[[], [], [], []], [[], [False], [], []], [[], [], [], []]], [[[False], [], [], []], [[False], [False], [], []], [[], [], [], []]], [[[], [], [], []], [[], [], [], []], [[], [], [], []]]],
#                 'room_objects': [[[],[],[]], [[],[],[['goalcolor',(-1,0)]]], [[],[['goalcolor',(0,-1)]],[]]],
#                 'room_objects_color': [[[], [], []], [[], [], ['green']], [[], ['blue'], []]],
#                 'width': None,
#                 'height': None}
#         super().__init__(
#             start_room = [1,0],
#             instrs = GoToGoalInstr(ObjDesc('box', 'blue')),#, room=end_room),
#             args=args,
#             steps_limit=50)

# class Level_Parallel2KeyTest(InvarianceTest):
#     """
#     Subtask A in transfer learning env setup
#     """

#     def __init__(self, seed=None, doors_per_side=3):
#         args = {'door_pos_lst': [[[[], [], [], []],   [[], [1], [], []],   [[],[],[],[]]], [[[1], [], [], []],   [[1], [1], [], []],   [[],[],[],[]]], [[[], [], [], []],   [[], [], [], []],   [[],[],[],[]]]],
#                 'door_color_lst':  [[[[], [], [], []], [[], ['yellow'], [], []], [[], [], [], []]], [[['red'], [], [], []], [['green'], ['blue'], [], []], [[], [], [], []]], [[[], [], [], []], [[], [], [], []], [[], [], [], []]]],
#                 'door_lock_lst': [[[[], [], [], []], [[], [False], [], []], [[], [], [], []]], [[[False], [], [], []], [[False], [False], [], []], [[], [], [], []]], [[[], [], [], []], [[], [], [], []], [[], [], [], []]]],
#                 'room_objects': [[[],[],[]], [[],[['key', 0]],[]], [[],[],[]]],
#                 'room_objects_color': [[[], [], []], [[], ['blue'], []], [[], [], []]],
#                 'width': None,
#                 'height': None}
#         super().__init__(
#             start_room = [1,0],
#             instrs =  OpenInstrTwoRoom(ObjDesc('door', 'blue'), room=[2,1]),
#             args=args,
#             steps_limit=50)





# Register the levels in this file
register_levels(__name__, globals())
