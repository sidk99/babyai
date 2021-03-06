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


class Level_OneRoomOneDoorRedTest(RoomGridLevel):
    """
    Go to the red door
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None):
        super().__init__(
            num_rows=1,
            num_cols=2,
            room_size=9,
            seed=seed
        )
        self.door_pos = 0
    def set_door_loc(self, door_pos):
        for j in range(0, self.num_rows):
            # For each column of rooms
            for i in range(0, self.num_cols):
                room = self.room_grid[j][i]

                x_l, y_l = (room.top[0] + 1, room.top[1] + 1)
                x_m, y_m = (room.top[0] + room.size[0] - 1, room.top[1] + room.size[1] - 1)
                # Door positions, order is right, down, left, up
                if i < self.num_cols - 1:
                    room.neighbors[0] = self.room_grid[j][i+1]
                    room.door_pos[0] = (x_m, y_l+door_pos)
                if j < self.num_rows - 1:
                    room.neighbors[1] = self.room_grid[j+1][i]
                    room.door_pos[1] = (x_l +door_pos, y_m)
                if i > 0:
                    room.neighbors[2] = self.room_grid[j][i-1]
                    room.door_pos[2] = room.neighbors[2].door_pos[0]
                if j > 0:
                    room.neighbors[3] = self.room_grid[j-1][i]
                    room.door_pos[3] = room.neighbors[3].door_pos[1]


    def gen_mission(self):
        #import pdb; pdb.set_trace()
        self.set_door_loc(0)
        obj, _ = self.add_door(0, 0,0,  'red', locked=False)
        self.place_agent(0, 0)
        self.instrs = OpenInstr(ObjDesc('door', 'red'), room = 1)

class Level_OneRoomTwoDoorTest(RoomGridLevel):
    """
    Go to the red door
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None, doors_per_side=3):
        self.doors_per_side=doors_per_side-1
        self.door_pos_lst = [[0,2],[],[],[]]
        self.door_color_lst = [['green', 'blue'], [], [], []]
        super().__init__(
            num_rows=1,
            num_cols=2,
            room_size=9,
            seed=seed
        )

    def _gen_grid(self, width, height):
        # Create the grid
        self.grid = Grid(width, height)
        print('BOOGIE WOOGIE')
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
                # room.door_pos = [[None]*self.doors_per_side]*4
                row.append(room)
                # Generate the walls for this room
                self.grid.wall_rect(*room.top, *room.size)

            self.room_grid.append(row)
        # For each row of rooms
        for j in range(0, self.num_rows):
            # For each column of rooms
            for i in range(0, self.num_cols):
                room = self.room_grid[j][i]

                x_l, y_l = (room.top[0] + 1, room.top[1] + 1)
                x_m, y_m = (room.top[0] + room.size[0] - 1, room.top[1] + room.size[1] - 1)
                x_piece = (x_m-x_l)/self.doors_per_side
                y_piece = (y_m-y_l)/self.doors_per_side
                print('Xpiece', x_piece)
                print('Ypiece', y_piece)
                # Door positions, order is right, down, left, up
                if i < self.num_cols - 1:
                    room.neighbors[0] = self.room_grid[j][i+1]
                    room.door_pos[0]=[] # room.door_pos is already [None]*4
                    for door_pos in self.door_pos_lst[0]:
                        room.door_pos[0].append((x_m, y_l+(door_pos*y_piece)))
                if j < self.num_rows - 1:
                    room.neighbors[1] = self.room_grid[j+1][i]
                    room.door_pos[1]=[]
                    for door_pos in self.door_pos_lst[1]:
                        room.door_pos[1].append(x_l+(door_pos*x_piece), y_m)
                if i > 0:
                    room.neighbors[2] = self.room_grid[j][i-1]
                    room.door_pos[2]=[]
                    for door_pos in self.door_pos_lst[2]:
                        room.door_pos[2].append(room.neighbors[2].door_pos[0])
                if j > 0:
                    room.neighbors[3] = self.room_grid[j-1][i]
                    room.door_pos[3]=[]
                    for door_pos in self.door_pos_lst[3]:
                        room.door_pos[3].append(room.neighbors[3].door_pos[1])
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
        print('BOOGIE WOOGIE')

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
        neighbor.doors[(door_idx+2) % 4] = door

        return door, pos

    # def reset(self, **kwargs):
    #     obs = super().reset(**kwargs)
    #
    #     # Recreate the verifier
    #     # self.instrs.reset_verifier(self)
    #
    #     # Compute the time step limit based on the maze size and instructions
    #     nav_time_room = self.room_size ** 2
    #     nav_time_maze = nav_time_room * self.num_rows * self.num_cols
    #     num_navs = self.num_navs_needed(self.instrs)
    #     self.max_steps = num_navs * nav_time_maze
    #
    #     return obs

    def gen_mission(self):
        # import pdb; pdb.set_trace()
        print('BOOGIE WOOGIE')
        # rightwalldoors=[0,9]
        #self.set_door_loc(0, rightwalldoors)
        for i in range(len(self.door_pos_lst)):
            for j in range(len(self.door_pos_lst[i])):
                obj, _ = self.add_door(0, 0,i,  self.door_color_lst[i][j], locked=False, doorid_on_idx=j)
        self.place_agent(0, 0)
        self.instrs = OpenInstr(ObjDesc('door', 'green'))

class Level_OneRoomTwoDoorBlueTest(RoomGridLevel):
    """
    Go to the red door
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None, doors_per_side=3):
        self.doors_per_side=doors_per_side-1
        self.door_pos_lst = [[0,2],[],[0],[]]
        self.door_color_lst = [['green', 'blue'], [], ['red'], []]
        super().__init__(
            num_rows=1,
            num_cols=2,
            room_size=9,
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
        for j in range(0, self.num_rows):
            # For each column of rooms
            for i in range(0, self.num_cols):
                room = self.room_grid[j][i]

                x_l, y_l = (room.top[0] + 1, room.top[1] + 1)
                x_m, y_m = (room.top[0] + room.size[0] - 1, room.top[1] + room.size[1] - 1)
                x_piece = (x_m-x_l)//self.doors_per_side
                y_piece = (y_m-y_l)//self.doors_per_side
                # Door positions, order is right, down, left, up
                if i < self.num_cols - 1:
                    room.neighbors[0] = self.room_grid[j][i+1]
                    room.door_pos[0]=[]
                    for door_pos in self.door_pos_lst[0]:
                        room.door_pos[0].append((x_m, y_l+(door_pos*y_piece)))
                    if i==0:
                        # room.neighbors[2] = self.room_grid[j][i-1]
                        room.door_pos[2]=[]
                        for door_pos in self.door_pos_lst[2]:
                            room.door_pos[2].append((x_l-1, y_l+(door_pos*y_piece)))
                if j < self.num_rows - 1:
                    room.neighbors[1] = self.room_grid[j+1][i]
                    room.door_pos[1]=[]
                    for door_pos in self.door_pos_lst[1]:
                        room.door_pos[1].append((x_l+(door_pos*x_piece), y_m))
                    if j==0:
                        # room.neighbors[3] = self.room_grid[j-1][i]
                        room.door_pos[3]=[]
                        for door_pos in self.door_pos_lst[3]:
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

    # def reset(self, **kwargs):
    #     obs = super().reset(**kwargs)
    #
    #     # Recreate the verifier
    #     # self.instrs.reset_verifier(self)
    #
    #     # Compute the time step limit based on the maze size and instructions
    #     nav_time_room = self.room_size ** 2
    #     nav_time_maze = nav_time_room * self.num_rows * self.num_cols
    #     num_navs = self.num_navs_needed(self.instrs)
    #     self.max_steps = num_navs * nav_time_maze
    #
    #     return obs

    def gen_mission(self):
        # import pdb; pdb.set_trace()
        print('BOOGIE WOOGIE')
        # rightwalldoors=[0,9]
        #self.set_door_loc(0, rightwalldoors)
        for i in range(len(self.door_pos_lst)):
            for j in range(len(self.door_pos_lst[i])):
                obj, _ = self.add_door(0, 0,i,  self.door_color_lst[i][j], locked=False, doorid_on_idx=j)
        self.place_agent(0, 0)
        self.instrs = OpenInstr(ObjDesc('door', 'blue'))

class Level_OneRoomTwoDoorGreenTest(RoomGridLevel):
    """
    Go to the red door
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None, doors_per_side=3):
        self.doors_per_side=doors_per_side-1
        self.door_pos_lst = [[0,2],[],[0],[]]
        self.door_color_lst = [['green', 'blue'], [], ['red'], []]
        super().__init__(
            num_rows=1,
            num_cols=2,
            room_size=9,
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
        for j in range(0, self.num_rows):
            # For each column of rooms
            for i in range(0, self.num_cols):
                room = self.room_grid[j][i]

                x_l, y_l = (room.top[0] + 1, room.top[1] + 1)
                x_m, y_m = (room.top[0] + room.size[0] - 1, room.top[1] + room.size[1] - 1)
                x_piece = (x_m-x_l)//self.doors_per_side
                y_piece = (y_m-y_l)//self.doors_per_side
                # Door positions, order is right, down, left, up
                if i < self.num_cols - 1:
                    room.neighbors[0] = self.room_grid[j][i+1]
                    room.door_pos[0]=[]
                    for door_pos in self.door_pos_lst[0]:
                        room.door_pos[0].append((x_m, y_l+(door_pos*y_piece)))
                    if i==0:
                        # room.neighbors[2] = self.room_grid[j][i-1]
                        room.door_pos[2]=[]
                        for door_pos in self.door_pos_lst[2]:
                            room.door_pos[2].append((x_l-1, y_l+(door_pos*y_piece)))
                if j < self.num_rows - 1:
                    room.neighbors[1] = self.room_grid[j+1][i]
                    room.door_pos[1]=[]
                    for door_pos in self.door_pos_lst[1]:
                        room.door_pos[1].append((x_l+(door_pos*x_piece), y_m))
                    if j==0:
                        # room.neighbors[3] = self.room_grid[j-1][i]
                        room.door_pos[3]=[]
                        for door_pos in self.door_pos_lst[3]:
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

    # def reset(self, **kwargs):
    #     obs = super().reset(**kwargs)
    #
    #     # Recreate the verifier
    #     # self.instrs.reset_verifier(self)
    #
    #     # Compute the time step limit based on the maze size and instructions
    #     nav_time_room = self.room_size ** 2
    #     nav_time_maze = nav_time_room * self.num_rows * self.num_cols
    #     num_navs = self.num_navs_needed(self.instrs)
    #     self.max_steps = num_navs * nav_time_maze
    #
    #     return obs

    def gen_mission(self):
        # import pdb; pdb.set_trace()
        print('BOOGIE WOOGIE')
        # rightwalldoors=[0,9]
        #self.set_door_loc(0, rightwalldoors)
        for i in range(len(self.door_pos_lst)):
            for j in range(len(self.door_pos_lst[i])):
                obj, _ = self.add_door(0, 0,i,  self.door_color_lst[i][j], locked=False, doorid_on_idx=j)
        self.place_agent(0, 0)
        self.instrs = OpenInstr(ObjDesc('door', 'green'))

class Level_OneRoomTwoDoorYellowTest(RoomGridLevel):
    """
    Go to the red door
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None, doors_per_side=3):
        self.doors_per_side=doors_per_side-1
        self.door_pos_lst = [[2],[],[0,2],[]]
        self.door_color_lst = [['yellow'], [], ['green', 'blue'], []]
        super().__init__(
            num_rows=1,
            num_cols=2,
            room_size=9,
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
        for j in range(0, self.num_rows):
            # For each column of rooms
            for i in range(0, self.num_cols):
                room = self.room_grid[j][i]

                x_l, y_l = (room.top[0] + 1, room.top[1] + 1)
                x_m, y_m = (room.top[0] + room.size[0] - 1, room.top[1] + room.size[1] - 1)
                x_piece = (x_m-x_l)//self.doors_per_side
                y_piece = (y_m-y_l)//self.doors_per_side
                # Door positions, order is right, down, left, up
                if i < self.num_cols - 1:
                    room.neighbors[0] = self.room_grid[j][i+1]
                    room.door_pos[0]=[]
                    for door_pos in self.door_pos_lst[0]:
                        room.door_pos[0].append((x_m, y_l+(door_pos*y_piece)))
                    if i==0:
                        # room.neighbors[2] = self.room_grid[j][i-1]
                        room.door_pos[2]=[]
                        for door_pos in self.door_pos_lst[2]:
                            room.door_pos[2].append((x_l-1, y_l+(door_pos*y_piece)))
                if j < self.num_rows - 1:
                    room.neighbors[1] = self.room_grid[j+1][i]
                    room.door_pos[1]=[]
                    for door_pos in self.door_pos_lst[1]:
                        room.door_pos[1].append((x_l+(door_pos*x_piece), y_m))
                    if j==0:
                        # room.neighbors[3] = self.room_grid[j-1][i]
                        room.door_pos[3]=[]
                        for door_pos in self.door_pos_lst[3]:
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

    # def reset(self, **kwargs):
    #     obs = super().reset(**kwargs)
    #
    #     # Recreate the verifier
    #     # self.instrs.reset_verifier(self)
    #
    #     # Compute the time step limit based on the maze size and instructions
    #     nav_time_room = self.room_size ** 2
    #     nav_time_maze = nav_time_room * self.num_rows * self.num_cols
    #     num_navs = self.num_navs_needed(self.instrs)
    #     self.max_steps = num_navs * nav_time_maze
    #
    #     return obs


    def gen_mission(self):
        # import pdb; pdb.set_trace()
        print('BOOGIE WOOGIE')
        # rightwalldoors=[0,9]
        #self.set_door_loc(0, rightwalldoors)
        for i in range(len(self.door_pos_lst)):
            for j in range(len(self.door_pos_lst[i])):
                obj, _ = self.add_door(0, 0,i,  self.door_color_lst[i][j], locked=False, doorid_on_idx=j)
        self.place_agent(0, 0)
        self.instrs = OpenInstr(ObjDesc('door', 'yellow'))

class Level_OLDThreeRoomTest(RoomGridLevel):
    """
    Go to the red doorThree
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None, doors_per_side=3):
        self.doors_per_side=doors_per_side-1
        self.door_pos_lst = [[[[0], [], [], []],[[0,2], [], [], []], [[2],[],[],[]]]]
        self.door_color_lst = [[[['red'], [], [], []], [['green', 'blue'], [], [], []], [[], [], [], []]]]
        super().__init__(
            num_rows=1,
            num_cols=3,
            room_size=9,
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

    # def reset(self, **kwargs):
    #     obs = super().reset(**kwargs)
    #
    #     # Recreate the verifier
    #     # self.instrs.reset_verifier(self)
    #
    #     # Compute the time step limit based on the maze size and instructions
    #     nav_time_room = self.room_size ** 2
    #     nav_time_maze = nav_time_room * self.num_rows * self.num_cols
    #     num_navs = self.num_navs_needed(self.instrs)
    #     self.max_steps = num_navs * nav_time_maze
    #
    #     return obs
    def add_object(self, i, j, kind=None, color=None):
       """
       Add a new object to room (i, j)
       """

       if kind == None:
           kind = self._rand_elem(['key', 'ball', 'box'])

       if color == None:
           color = self._rand_color()

       # TODO: we probably want to add an Object.make helper function
       assert kind in ['key', 'ball', 'box', 'goal']
       if kind == 'key':
           obj = Key(color)
       elif kind == 'ball':
           obj = Ball(color)
       elif kind == 'box':
           obj = Box(color)
       elif kind =='goal':
           obj = Goal()

       return self.place_in_room(i, j, obj)


    def gen_mission(self):
        # import pdb; pdb.set_trace()
        print('BOOGIE WOOGIE')
        # rightwalldoors=[0,9]
        #self.set_door_loc(0, rightwalldoors)
        for r in range(0, self.num_rows):
            # For each column of rooms
            for c in range(0, self.num_cols):
                room_door_pos_lst = self.door_pos_lst[r][c]
                room_door_color_lst = self.door_color_lst[r][c]
                for i in range(len(room_door_pos_lst)):
                    for j in range(len(room_door_pos_lst[i])):
                        print(room_door_color_lst[i][j])
                        # import pdb; pdb.set_trace()
                        obj, _ = self.add_door(c, r,i,  room_door_color_lst[i][j], locked=False, doorid_on_idx=j)
        self.place_agent(0, 0)
        self.instrs = OpenInstr(ObjDesc('door', 'yellow'))


class Level_RedDoorFourRoomTest(RoomGridLevel):
    """
    Go to the red doorThree
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None, doors_per_side=3):
        self.doors_per_side=doors_per_side-1
        self.door_pos_lst = [[[[0], [], [], []],[[0,2], [], [], []], [[2],[],[],[]], [[],[],[],[]]]]
        self.door_color_lst = [[[['red'], [], [], []], [['green', 'blue'], [], [], []], [['yellow'], [], [], []], [[],[],[],[]]]]
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

    # def reset(self, **kwargs):
    #     obs = super().reset(**kwargs)
    #
    #     # Recreate the verifier
    #     # self.instrs.reset_verifier(self)
    #
    #     # Compute the time step limit based on the maze size and instructions
    #     nav_time_room = self.room_size ** 2
    #     nav_time_maze = nav_time_room * self.num_rows * self.num_cols
    #     num_navs = self.num_navs_needed(self.instrs)
    #     self.max_steps = num_navs * nav_time_maze
    #
    #     return obs

    def gen_mission(self):
        # import pdb; pdb.set_trace()
        start_room = 0
        end_room = 1
        # rightwalldoors=[0,9]
        #self.set_door_loc(0, rightwalldoors)
        for r in range(0, self.num_rows):
            # For each column of rooms
            for c in range(0, self.num_cols):
                room_door_pos_lst = self.door_pos_lst[r][c]
                room_door_color_lst = self.door_color_lst[r][c]
                for i in range(len(room_door_pos_lst)):
                    for j in range(len(room_door_pos_lst[i])):
                        # print(room_door_color_lst[i][j])
                        # import pdb; pdb.set_trace()
                        obj, _ = self.add_door(c, r,i,  room_door_color_lst[i][j], locked=False, doorid_on_idx=j)
        self.place_agent(start_room,0)
        self.instrs = OpenInstr(ObjDesc('door', 'red'), room=end_room)



class Level_GreenDoorFourRoomTest(RoomGridLevel):
    """
    Go to the red doorThree
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None, doors_per_side=3):
        self.doors_per_side=doors_per_side-1
        self.door_pos_lst = [[[[0], [], [], []],[[0,2], [], [], []], [[2],[],[],[]], [[],[],[],[]]]]
        self.door_color_lst = [[[['red'], [], [], []], [['green', 'blue'], [], [], []], [['yellow'], [], [], []], [[],[],[],[]]]]
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

    # def reset(self, **kwargs):
    #     obs = super().reset(**kwargs)
    #
    #     # Recreate the verifier
    #     # self.instrs.reset_verifier(self)
    #
    #     # Compute the time step limit based on the maze size and instructions
    #     nav_time_room = self.room_size ** 2
    #     nav_time_maze = nav_time_room * self.num_rows * self.num_cols
    #     num_navs = self.num_navs_needed(self.instrs)
    #     self.max_steps = num_navs * nav_time_maze
    #
    #     return obs

    def gen_mission(self):
        # import pdb; pdb.set_trace()
        start_room = 1
        end_room = 2
        # rightwalldoors=[0,9]
        #self.set_door_loc(0, rightwalldoors)
        for r in range(0, self.num_rows):
            # For each column of rooms
            for c in range(0, self.num_cols):
                room_door_pos_lst = self.door_pos_lst[r][c]
                room_door_color_lst = self.door_color_lst[r][c]
                for i in range(len(room_door_pos_lst)):
                    for j in range(len(room_door_pos_lst[i])):
                        # print(room_door_color_lst[i][j])
                        # import pdb; pdb.set_trace()
                        obj, _ = self.add_door(c, r,i,  room_door_color_lst[i][j], locked=False, doorid_on_idx=j)
        self.place_agent(start_room,0)
        self.instrs = OpenInstr(ObjDesc('door', 'green'), room=end_room)


class Level_RedGreenDoorFourRoomTest(RoomGridLevel):
    """
    Go to the red doorThree
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None, doors_per_side=3):
        self.doors_per_side=doors_per_side-1
        self.door_pos_lst = [[[[0], [], [], []],[[0,2], [], [], []], [[2],[],[],[]], [[],[],[],[]]]]
        self.door_color_lst = [[[['red'], [], [], []], [['green', 'blue'], [], [], []], [['yellow'], [], [], []], [[],[],[],[]]]]
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

    # def reset(self, **kwargs):
    #     obs = super().reset(**kwargs)
    #
    #     # Recreate the verifier
    #     # self.instrs.reset_verifier(self)
    #
    #     # Compute the time step limit based on the maze size and instructions
    #     nav_time_room = self.room_size ** 2
    #     nav_time_maze = nav_time_room * self.num_rows * self.num_cols
    #     num_navs = self.num_navs_needed(self.instrs)
    #     self.max_steps = num_navs * nav_time_maze
    #
    #     return obs

    def gen_mission(self):
        # import pdb; pdb.set_trace()
        start_room = 0
        end_room = 2
        # rightwalldoors=[0,9]
        #self.set_door_loc(0, rightwalldoors)
        for r in range(0, self.num_rows):
            # For each column of rooms
            for c in range(0, self.num_cols):
                room_door_pos_lst = self.door_pos_lst[r][c]
                room_door_color_lst = self.door_color_lst[r][c]
                for i in range(len(room_door_pos_lst)):
                    for j in range(len(room_door_pos_lst[i])):
                        # print(room_door_color_lst[i][j])
                        # import pdb; pdb.set_trace()
                        obj, _ = self.add_door(c, r,i,  room_door_color_lst[i][j], locked=False, doorid_on_idx=j)
        self.place_agent(start_room,0)
        self.instrs = OpenInstr(ObjDesc('door', 'green'), room=end_room)




class Level_BlueDoorFourRoomTest(RoomGridLevel):
    """
    Go to the red doorThree
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None, doors_per_side=3):
        self.doors_per_side=doors_per_side-1
        self.door_pos_lst = [[[[0], [], [], []],[[0,2], [], [], []], [[2],[],[],[]], [[],[],[],[]]]]
        self.door_color_lst = [[[['red'], [], [], []], [['green', 'blue'], [], [], []], [['yellow'], [], [], []], [[],[],[],[]]]]
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

    # def reset(self, **kwargs):
    #     obs = super().reset(**kwargs)
    #
    #     # Recreate the verifier
    #     # self.instrs.reset_verifier(self)
    #
    #     # Compute the time step limit based on the maze size and instructions
    #     nav_time_room = self.room_size ** 2
    #     nav_time_maze = nav_time_room * self.num_rows * self.num_cols
    #     num_navs = self.num_navs_needed(self.instrs)
    #     self.max_steps = num_navs * nav_time_maze
    #
    #     return obs

    def gen_mission(self):
        # import pdb; pdb.set_trace()
        start_room = 1
        end_room = 2
        # rightwalldoors=[0,9]
        #self.set_door_loc(0, rightwalldoors)
        for r in range(0, self.num_rows):
            # For each column of rooms
            for c in range(0, self.num_cols):
                room_door_pos_lst = self.door_pos_lst[r][c]
                room_door_color_lst = self.door_color_lst[r][c]
                for i in range(len(room_door_pos_lst)):
                    for j in range(len(room_door_pos_lst[i])):
                        # print(room_door_color_lst[i][j])
                        # import pdb; pdb.set_trace()
                        obj, _ = self.add_door(c, r,i,  room_door_color_lst[i][j], locked=False, doorid_on_idx=j)
        self.place_agent(start_room,0)
        self.instrs = OpenInstr(ObjDesc('door', 'blue'), room=end_room)



class Level_YellowDoorFourRoomTest(RoomGridLevel):
    """
    Go to the red doorThree
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None, doors_per_side=3):
        self.doors_per_side=doors_per_side-1
        self.door_pos_lst = [[[[0], [], [], []],[[0,2], [], [], []], [[2],[],[],[]], [[],[],[],[]]]]
        self.door_color_lst = [[[['red'], [], [], []], [['green', 'blue'], [], [], []], [['yellow'], [], [], []], [[],[],[],[]]]]
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

    # def reset(self, **kwargs):
    #     obs = super().reset(**kwargs)
    #
    #     # Recreate the verifier
    #     # self.instrs.reset_verifier(self)
    #
    #     # Compute the time step limit based on the maze size and instructions
    #     nav_time_room = self.room_size ** 2
    #     nav_time_maze = nav_time_room * self.num_rows * self.num_cols
    #     num_navs = self.num_navs_needed(self.instrs)
    #     self.max_steps = num_navs * nav_time_maze
    #
    #     return obs

    def gen_mission(self):
        # import pdb; pdb.set_trace()
        start_room = 2
        end_room = 3
        # rightwalldoors=[0,9]
        #self.set_door_loc(0, rightwalldoors)
        for r in range(0, self.num_rows):
            # For each column of rooms
            for c in range(0, self.num_cols):
                room_door_pos_lst = self.door_pos_lst[r][c]
                room_door_color_lst = self.door_color_lst[r][c]
                for i in range(len(room_door_pos_lst)):
                    for j in range(len(room_door_pos_lst[i])):
                        # print(room_door_color_lst[i][j])
                        # import pdb; pdb.set_trace()
                        obj, _ = self.add_door(c, r,i,  room_door_color_lst[i][j], locked=False, doorid_on_idx=j)
        self.place_agent(start_room,0)
        self.instrs = OpenInstr(ObjDesc('door', 'yellow'), room=end_room)


class Level_FourRoomTest(RoomGridLevel):
    """
    Go to the red doorThree
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None, doors_per_side=3):
        self.doors_per_side=doors_per_side-1
        self.door_pos_lst = [[[[0], [], [], []],[[0,2], [], [], []], [[2],[],[],[]], [[],[],[],[]]]]
        self.door_color_lst = [[[['red'], [], [], []], [['green', 'blue'], [], [], []], [['yellow'], [], [], []], [[],[],[],[]]]]
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

    # def reset(self, **kwargs):
    #     obs = super().reset(**kwargs)
    #
    #     # Recreate the verifier
    #     # self.instrs.reset_verifier(self)
    #
    #     # Compute the time step limit based on the maze size and instructions
    #     nav_time_room = self.room_size ** 2
    #     nav_time_maze = nav_time_room * self.num_rows * self.num_cols
    #     num_navs = self.num_navs_needed(self.instrs)
    #     self.max_steps = num_navs * nav_time_maze
    #
    #     return obs

    def gen_mission(self):
        # import pdb; pdb.set_trace()
        start_room = 0
        end_room = 3
        # rightwalldoors=[0,9]
        #self.set_door_loc(0, rightwalldoors)
        for r in range(0, self.num_rows):
            # For each column of rooms
            for c in range(0, self.num_cols):
                room_door_pos_lst = self.door_pos_lst[r][c]
                room_door_color_lst = self.door_color_lst[r][c]
                for i in range(len(room_door_pos_lst)):
                    for j in range(len(room_door_pos_lst[i])):
                        # print(room_door_color_lst[i][j])
                        # import pdb; pdb.set_trace()
                        obj, _ = self.add_door(c, r,i,  room_door_color_lst[i][j], locked=False, doorid_on_idx=j)
        self.place_agent(start_room,0)
        self.instrs = OpenInstr(ObjDesc('door', 'yellow'), room=end_room)


class Level_GreenKeyFourRoomTest(RoomGridLevel):
    """
    Go to the red doorThree
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None, doors_per_side=3):
        self.doors_per_side=doors_per_side-1
        self.door_pos_lst = [[[[0], [], [], []],[[0,2], [], [], []], [[2],[],[],[]], [[],[],[],[]]]]
        self.door_color_lst = [[[['red'], [], [], []], [['green', 'blue'], [], [], []], [['yellow'], [], [], []], [[],[],[],[]]]]
        self.door_lock_lst = [[[[False], [], [], []], [[True, True], [], [], []], [[False], [], [], []], [[],[],[],[]]]]
        self.room_objects = [[[],['key'],[],[]]]
        self.room_objects_color = [[[], ['green'], [], []]]
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

    # def reset(self, **kwargs):
    #     obs = super().reset(**kwargs)
    #
    #     # Recreate the verifier
    #     # self.instrs.reset_verifier(self)
    #
    #     # Compute the time step limit based on the maze size and instructions
    #     nav_time_room = self.room_size ** 2
    #     nav_time_maze = nav_time_room * self.num_rows * self.num_cols
    #     num_navs = self.num_navs_needed(self.instrs)
    #     self.max_steps = num_navs * nav_time_maze
    #
    #     return obs

    def gen_mission(self):
        # import pdb; pdb.set_trace()
        start_room = 0
        end_room = 3
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
                    self.add_object(c, r, kind=obj, color=self.room_objects_color[r][c][idx])
        self.place_agent(start_room,0)
        self.instrs = OpenInstr(ObjDesc('door', 'yellow'), room=end_room)


class Level_BlueKeyFourRoomTest(RoomGridLevel):
    """
    Go to the red doorThree
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None, doors_per_side=3):
        self.doors_per_side=doors_per_side-1
        self.door_pos_lst = [[[[0], [], [], []],[[0,2], [], [], []], [[2],[],[],[]], [[],[],[],[]]]]
        self.door_color_lst = [[[['red'], [], [], []], [['green', 'blue'], [], [], []], [['yellow'], [], [], []], [[],[],[],[]]]]
        self.door_lock_lst = [[[[False], [], [], []], [[True, True], [], [], []], [[False], [], [], []], [[],[],[],[]]]]
        self.room_objects = [[[],['key'],[],[]]]
        self.room_objects_color = [[[], ['blue'], [], []]]
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

    # def reset(self, **kwargs):
    #     obs = super().reset(**kwargs)
    #
    #     # Recreate the verifier
    #     # self.instrs.reset_verifier(self)
    #
    #     # Compute the time step limit based on the maze size and instructions
    #     nav_time_room = self.room_size ** 2
    #     nav_time_maze = nav_time_room * self.num_rows * self.num_cols
    #     num_navs = self.num_navs_needed(self.instrs)
    #     self.max_steps = num_navs * nav_time_maze
    #
    #     return obs

    def gen_mission(self):
        # import pdb; pdb.set_trace()
        start_room = 0
        end_room = 3
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
                    self.add_object(c, r, kind=obj, color=self.room_objects_color[r][c][idx])
        self.place_agent(start_room,0)
        self.instrs = OpenInstr(ObjDesc('door', 'yellow'), room=end_room)

class Level_RedDoorThreeRoomTest(RoomGridLevel):
    """
    Go to the red doorThree
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None, doors_per_side=3):
        self.doors_per_side=doors_per_side-1
        self.door_pos_lst = [[[[0], [], [], []],[[0,2], [], [], []], [[],[],[],[]]]]
        self.door_color_lst = [[[['red'], [], [], []], [['green', 'blue'], [], [], []], [[], [], [], []]]]
        self.door_lock_lst = [[[[False], [], [], []], [[True, True], [], [], []], [[], [], [], []]]]
        self.room_objects = [[[],[],[]]]
        self.room_objects_color = [[[], [], []]]
        super().__init__(
            num_rows=1,
            num_cols=3,
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

    # def reset(self, **kwargs):
    #     obs = super().reset(**kwargs)
    #
    #     # Recreate the verifier
    #     # self.instrs.reset_verifier(self)
    #
    #     # Compute the time step limit based on the maze size and instructions
    #     nav_time_room = self.room_size ** 2
    #     nav_time_maze = nav_time_room * self.num_rows * self.num_cols
    #     num_navs = self.num_navs_needed(self.instrs)
    #     self.max_steps = num_navs * nav_time_maze
    #
    #     return obs

    def gen_mission(self):
        # import pdb; pdb.set_trace()
        start_room = 0
        end_room = 1
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
                    self.add_object(c, r, kind=obj, color=self.room_objects_color[r][c][idx])
        self.place_agent(start_room,0)
        self.instrs = OpenInstr(ObjDesc('door', 'red'), room=end_room)

class Level_RedDoorRedKeyThreeRoomTest(RoomGridLevel):
    """
    Go to the red doorThree
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None, doors_per_side=3):
        self.doors_per_side=doors_per_side-1
        self.door_pos_lst = [[[[0], [], [], []],[[0,2], [], [], []], [[],[],[],[]]]]
        self.door_color_lst = [[[['red'], [], [], []], [['green', 'blue'], [], [], []], [[], [], [], []]]]
        self.door_lock_lst = [[[[False], [], [], []], [[True, True], [], [], []], [[], [], [], []]]]
        self.room_objects = [[['key'],[],[]]]
        self.room_objects_color = [[['red'], [], []]]
        super().__init__(
            num_rows=1,
            num_cols=3,
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

    # def reset(self, **kwargs):
    #     obs = super().reset(**kwargs)
    #
    #     # Recreate the verifier
    #     # self.instrs.reset_verifier(self)
    #
    #     # Compute the time step limit based on the maze size and instructions
    #     nav_time_room = self.room_size ** 2
    #     nav_time_maze = nav_time_room * self.num_rows * self.num_cols
    #     num_navs = self.num_navs_needed(self.instrs)
    #     self.max_steps = num_navs * nav_time_maze
    #
    #     return obs

    def gen_mission(self):
        # import pdb; pdb.set_trace()
        start_room = 0
        end_room = 1
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
                    self.add_object(c, r, kind=obj, color=self.room_objects_color[r][c][idx])
        self.place_agent(start_room,0)
        self.instrs = OpenInstr(ObjDesc('door', 'red'), room=end_room)


class Level_GreenKeyGreenDoorThreeRoomTest(RoomGridLevel):
    """
    Go to the red doorThree
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None, doors_per_side=3):
        self.doors_per_side=doors_per_side-1
        self.door_pos_lst = [[[[0], [], [], []],[[0,2], [], [], []], [[],[],[],[]]]]
        self.door_color_lst = [[[['red'], [], [], []], [['green', 'blue'], [], [], []], [[], [], [], []]]]
        self.door_lock_lst = [[[[False], [], [], []], [[True, True], [], [], []], [[], [], [], []]]]
        self.room_objects = [[[],['key'],[]]]
        self.room_objects_color = [[[], ['green'], []]]
        super().__init__(
            num_rows=1,
            num_cols=3,
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

    # def reset(self, **kwargs):
    #     obs = super().reset(**kwargs)
    #
    #     # Recreate the verifier
    #     # self.instrs.reset_verifier(self)
    #
    #     # Compute the time step limit based on the maze size and instructions
    #     nav_time_room = self.room_size ** 2
    #     nav_time_maze = nav_time_room * self.num_rows * self.num_cols
    #     num_navs = self.num_navs_needed(self.instrs)
    #     self.max_steps = num_navs * nav_time_maze
    #
    #     return obs

    def gen_mission(self):
        # import pdb; pdb.set_trace()
        start_room = 1
        end_room = 2
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
                    self.add_object(c, r, kind=obj, color=self.room_objects_color[r][c][idx])
        self.place_agent(start_room,0)
        self.instrs = OpenInstr(ObjDesc('door', 'green'), room=end_room)

class Level_BlueKeyBlueDoorThreeRoomTest(RoomGridLevel):
    """
    Go to the red doorThree
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None, doors_per_side=3):
        self.doors_per_side=doors_per_side-1
        self.door_pos_lst = [[[[0], [], [], []],[[0,2], [], [], []], [[],[],[],[]]]]
        self.door_color_lst = [[[['red'], [], [], []], [['green', 'blue'], [], [], []], [[], [], [], []]]]
        self.door_lock_lst = [[[[False], [], [], []], [[True, True], [], [], []], [[], [], [], []]]]
        self.room_objects = [[[],['key'],[]]]
        self.room_objects_color = [[[], ['blue'], []]]
        super().__init__(
            num_rows=1,
            num_cols=3,
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

    # def reset(self, **kwargs):
    #     obs = super().reset(**kwargs)
    #
    #     # Recreate the verifier
    #     # self.instrs.reset_verifier(self)
    #
    #     # Compute the time step limit based on the maze size and instructions
    #     nav_time_room = self.room_size ** 2
    #     nav_time_maze = nav_time_room * self.num_rows * self.num_cols
    #     num_navs = self.num_navs_needed(self.instrs)
    #     self.max_steps = num_navs * nav_time_maze
    #
    #     return obs

    def gen_mission(self):
        # import pdb; pdb.set_trace()
        start_room = 1
        end_room = 2
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
                    self.add_object(c, r, kind=obj, color=self.room_objects_color[r][c][idx])
        self.place_agent(start_room,0)
        self.instrs = OpenInstr(ObjDesc('door', 'blue'), room=end_room)



class Level_BlueThreeRoomTest(RoomGridLevel):
    """
    Go to the red doorThree
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None, doors_per_side=3):
        self.doors_per_side=doors_per_side-1
        self.door_pos_lst = [[[[0], [], [], []],[[0,2], [], [], []], [[],[],[],[]]]]
        self.door_color_lst = [[[['red'], [], [], []], [['green', 'blue'], [], [], []], [[], [], [], []]]]
        self.door_lock_lst = [[[[False], [], [], []], [[True, False], [], [], []], [[], [], [], []]]]
        self.room_objects = [[[],[],['goal']]]
        self.room_objects_color = [[[], [], ['green']]]
        super().__init__(
            num_rows=1,
            num_cols=3,
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

    # def reset(self, **kwargs):
    #     obs = super().reset(**kwargs)
    #
    #     # Recreate the verifier
    #     # self.instrs.reset_verifier(self)
    #
    #     # Compute the time step limit based on the maze size and instructions
    #     nav_time_room = self.room_size ** 2
    #     nav_time_maze = nav_time_room * self.num_rows * self.num_cols
    #     num_navs = self.num_navs_needed(self.instrs)
    #     self.max_steps = num_navs * nav_time_maze
    #
    #     return obs
    def add_object(self, i, j, kind=None, color=None):
       """
       Add a new object to room (i, j)
       """

       if kind == None:
           kind = self._rand_elem(['key', 'ball', 'box'])

       if color == None:
           color = self._rand_color()

       # TODO: we probably want to add an Object.make helper function
       assert kind in ['key', 'ball', 'box', 'goal']
       if kind == 'key':
           obj = Key(color)
       elif kind == 'ball':
           obj = Ball(color)
       elif kind == 'box':
           obj = Box(color)
       elif kind =='goal':
           obj = Goal()

       return self.place_in_room(i, j, obj)

    def gen_mission(self):
        # import pdb; pdb.set_trace()
        start_room = 0
        end_room = 2
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
                    self.add_object(c, r, kind=obj, color=self.room_objects_color[r][c][idx])
        self.place_agent(start_room,0)
        self.instrs = GoToGoalInstr(ObjDesc('goal', 'green'))#, room=end_room)

        # self.instrs = OpenInstr(ObjDesc('door', 'red'), room=end_room)
class Level_GreenThreeRoomTest(RoomGridLevel):
    """
    Go to the red doorThree
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None, doors_per_side=3):
        self.doors_per_side=doors_per_side-1
        self.door_pos_lst = [[[[0], [], [], []],[[0,2], [], [], []], [[],[],[],[]]]]
        self.door_color_lst = [[[['red'], [], [], []], [['green', 'blue'], [], [], []], [[], [], [], []]]]
        self.door_lock_lst = [[[[False], [], [], []], [[False, True], [], [], []], [[], [], [], []]]]
        self.room_objects = [[[],[],['goal']]]
        self.room_objects_color = [[[], [], ['green']]]
        super().__init__(
            num_rows=1,
            num_cols=3,
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

    # def reset(self, **kwargs):
    #     obs = super().reset(**kwargs)
    #
    #     # Recreate the verifier
    #     # self.instrs.reset_verifier(self)
    #
    #     # Compute the time step limit based on the maze size and instructions
    #     nav_time_room = self.room_size ** 2
    #     nav_time_maze = nav_time_room * self.num_rows * self.num_cols
    #     num_navs = self.num_navs_needed(self.instrs)
    #     self.max_steps = num_navs * nav_time_maze
    #
    #     return obs
    def add_object(self, i, j, kind=None, color=None):
       """
       Add a new object to room (i, j)
       """

       if kind == None:
           kind = self._rand_elem(['key', 'ball', 'box'])

       if color == None:
           color = self._rand_color()

       # TODO: we probably want to add an Object.make helper function
       assert kind in ['key', 'ball', 'box', 'goal']
       if kind == 'key':
           obj = Key(color)
       elif kind == 'ball':
           obj = Ball(color)
       elif kind == 'box':
           obj = Box(color)
       elif kind =='goal':
           obj = Goal()

       return self.place_in_room(i, j, obj)

    def gen_mission(self):
        # import pdb; pdb.set_trace()
        start_room = 0
        end_room = 2
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
                    self.add_object(c, r, kind=obj, color=self.room_objects_color[r][c][idx])
        self.place_agent(start_room,0)
        self.instrs = GoToGoalInstr(ObjDesc('goal', 'blue'))#, room=end_room)

        # self.instrs = OpenInstr(ObjDesc('door', 'red'), room=end_room)


class Level_GreenDoorThreeRoomTest(RoomGridLevel):
    """
    Go to the red doorThree
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None, doors_per_side=3):
        self.doors_per_side=doors_per_side-1
        self.door_pos_lst = [[[[0], [], [], []],[[0,2], [], [], []], [[],[],[],[]]]]
        self.door_color_lst = [[[['red'], [], [], []], [['green', 'blue'], [], [], []], [[], [], [], []]]]
        self.door_lock_lst = [[[[False], [], [], []], [[False, True], [], [], []], [[], [], [], []]]]
        self.room_objects = [[[],[],['goal']]]
        self.room_objects_color = [[[], [], ['green']]]
        super().__init__(
            num_rows=1,
            num_cols=3,
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

    # def reset(self, **kwargs):
    #     obs = super().reset(**kwargs)
    #
    #     # Recreate the verifier
    #     # self.instrs.reset_verifier(self)
    #
    #     # Compute the time step limit based on the maze size and instructions
    #     nav_time_room = self.room_size ** 2
    #     nav_time_maze = nav_time_room * self.num_rows * self.num_cols
    #     num_navs = self.num_navs_needed(self.instrs)
    #     self.max_steps = num_navs * nav_time_maze
    #
    #     return obs
    def add_object(self, i, j, kind=None, color=None):
       """
       Add a new object to room (i, j)
       """

       if kind == None:
           kind = self._rand_elem(['key', 'ball', 'box'])

       if color == None:
           color = self._rand_color()

       # TODO: we probably want to add an Object.make helper function
       assert kind in ['key', 'ball', 'box', 'goal']
       if kind == 'key':
           obj = Key(color)
       elif kind == 'ball':
           obj = Ball(color)
       elif kind == 'box':
           obj = Box(color)
       elif kind =='goal':
           obj = Goal()

       return self.place_in_room(i, j, obj)

    def gen_mission(self):
        # import pdb; pdb.set_trace()
        start_room = 1
        end_room = 2
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
                    self.add_object(c, r, kind=obj, color=self.room_objects_color[r][c][idx])
        self.place_agent(start_room,0)
        self.instrs = GoToGoalInstr(ObjDesc('goal', 'green'))#, room=end_room)

        # self.instrs = OpenInstr(ObjDesc('door', 'green'), room=end_room)


class Level_BlueDoorThreeRoomTest(RoomGridLevel):
    """
    Go to the red doorThree
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None, doors_per_side=3):
        self.doors_per_side=doors_per_side-1
        self.door_pos_lst = [[[[0], [], [], []],[[0,2], [], [], []], [[],[],[],[]]]]
        self.door_color_lst = [[[['red'], [], [], []], [['green', 'blue'], [], [], []], [[], [], [], []]]]
        self.door_lock_lst = [[[[False], [], [], []], [[True, False], [], [], []], [[], [], [], []]]]
        self.room_objects = [[[],[],['goal']]]
        self.room_objects_color = [[[], [], ['green']]]
        super().__init__(
            num_rows=1,
            num_cols=3,
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

    # def reset(self, **kwargs):
    #     obs = super().reset(**kwargs)
    #
    #     # Recreate the verifier
    #     # self.instrs.reset_verifier(self)
    #
    #     # Compute the time step limit based on the maze size and instructions
    #     nav_time_room = self.room_size ** 2
    #     nav_time_maze = nav_time_room * self.num_rows * self.num_cols
    #     num_navs = self.num_navs_needed(self.instrs)
    #     self.max_steps = num_navs * nav_time_maze
    #
    #     return obs
    def add_object(self, i, j, kind=None, color=None):
       """
       Add a new object to room (i, j)
       """

       if kind == None:
           kind = self._rand_elem(['key', 'ball', 'box'])

       if color == None:
           color = self._rand_color()

       # TODO: we probably want to add an Object.make helper function
       assert kind in ['key', 'ball', 'box', 'goal']
       if kind == 'key':
           obj = Key(color)
       elif kind == 'ball':
           obj = Ball(color)
       elif kind == 'box':
           obj = Box(color)
       elif kind =='goal':
           obj = Goal()

       return self.place_in_room(i, j, obj)


    def gen_mission(self):
        # import pdb; pdb.set_trace()
        start_room = 1
        end_room = 2
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
                    self.add_object(c, r, kind=obj, color=self.room_objects_color[r][c][idx])
        self.place_agent(start_room,0)
        self.instrs = GoToGoalInstr(ObjDesc('goal', 'green'))#, room=end_room)

class Level_GreenKeyThreeRoomTest(RoomGridLevel):
    """
    Go to the red doorThree
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None, doors_per_side=3):
        self.doors_per_side=doors_per_side-1
        self.door_pos_lst = [[[[0], [], [], []],[[0,2], [], [], []], [[],[],[],[]]]]
        self.door_color_lst = [[[['red'], [], [], []], [['green', 'blue'], [], [], []], [[], [], [], []]]]
        self.door_lock_lst = [[[[False], [], [], []], [[True, True], [], [], []], [[], [], [], []]]]
        self.room_objects = [[[],['key'],[]]]
        self.room_objects_color = [[[], ['green'], []]]
        super().__init__(
            num_rows=1,
            num_cols=3,
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

    # def reset(self, **kwargs):
    #     obs = super().reset(**kwargs)
    #
    #     # Recreate the verifier
    #     # self.instrs.reset_verifier(self)
    #
    #     # Compute the time step limit based on the maze size and instructions
    #     nav_time_room = self.room_size ** 2
    #     nav_time_maze = nav_time_room * self.num_rows * self.num_cols
    #     num_navs = self.num_navs_needed(self.instrs)
    #     self.max_steps = num_navs * nav_time_maze
    #
    #     return obs

    def gen_mission(self):
        # import pdb; pdb.set_trace()
        start_room = 0
        end_room = 2
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
                    self.add_object(c, r, kind=obj, color=self.room_objects_color[r][c][idx])
        self.place_agent(start_room,0)
        self.instrs = OpenInstr(ObjDesc('door', 'green'), room=end_room)


class Level_GreenKeyGreenDoorBallThreeRoomTest(RoomGridLevel):
    """
    Go to the red doorThree
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None, doors_per_side=3):
        self.doors_per_side=doors_per_side-1
        self.door_pos_lst = [[[[0], [], [], []],[[0,2], [], [], []], [[],[],[],[]]]]
        self.door_color_lst = [[[['red'], [], [], []], [['green', 'blue'], [], [], []], [[], [], [], []]]]
        self.door_lock_lst = [[[[False], [], [], []], [[True, True], [], [], []], [[], [], [], []]]]
        self.room_objects = [[[],['key'],['ball']]]
        self.room_objects_color = [[[], ['green'], ['yellow']]]
        super().__init__(
            num_rows=1,
            num_cols=3,
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

    # def reset(self, **kwargs):
    #     obs = super().reset(**kwargs)
    #
    #     # Recreate the verifier
    #     # self.instrs.reset_verifier(self)
    #
    #     # Compute the time step limit based on the maze size and instructions
    #     nav_time_room = self.room_size ** 2
    #     nav_time_maze = nav_time_room * self.num_rows * self.num_cols
    #     num_navs = self.num_navs_needed(self.instrs)
    #     self.max_steps = num_navs * nav_time_maze
    #
    #     return obs

    def gen_mission(self):
        # import pdb; pdb.set_trace()
        start_room = 1
        end_room = 2
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
                    self.add_object(c, r, kind=obj, color=self.room_objects_color[r][c][idx])
        self.place_agent(start_room,0)
        # self.instrs = OpenInstr(ObjDesc('door', 'blue'), room=end_room)
        self.instrs = PickupInstr(ObjDesc('ball'))




class Level_BlueKeyThreeRoomTest(RoomGridLevel):
    """
    Go to the red doorThree
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None, doors_per_side=3):
        self.doors_per_side=doors_per_side-1
        self.door_pos_lst = [[[[0], [], [], []],[[0,2], [], [], []], [[],[],[],[]]]]
        self.door_color_lst = [[[['red'], [], [], []], [['green', 'blue'], [], [], []], [[], [], [], []]]]
        self.door_lock_lst = [[[[False], [], [], []], [[True, True], [], [], []], [[], [], [], []]]]
        self.room_objects = [[[],['key'],[]]]
        self.room_objects_color = [[[], ['blue'], []]]
        super().__init__(
            num_rows=1,
            num_cols=3,
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

    # def reset(self, **kwargs):
    #     obs = super().reset(**kwargs)
    #
    #     # Recreate the verifier
    #     # self.instrs.reset_verifier(self)
    #
    #     # Compute the time step limit based on the maze size and instructions
    #     nav_time_room = self.room_size ** 2
    #     nav_time_maze = nav_time_room * self.num_rows * self.num_cols
    #     num_navs = self.num_navs_needed(self.instrs)
    #     self.max_steps = num_navs * nav_time_maze
    #
    #     return obs

    def gen_mission(self):
        # import pdb; pdb.set_trace()
        start_room = 0
        end_room = 2
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
                    self.add_object(c, r, kind=obj, color=self.room_objects_color[r][c][idx])
        self.place_agent(start_room,0)
        self.instrs = OpenInstr(ObjDesc('door', 'blue'), room=end_room)


class Level_BlueKeyBlueDoorBallThreeRoomTest(RoomGridLevel):
    """
    Go to the red doorThree
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None, doors_per_side=3):
        self.doors_per_side=doors_per_side-1
        self.door_pos_lst = [[[[0], [], [], []],[[0,2], [], [], []], [[],[],[],[]]]]
        self.door_color_lst = [[[['red'], [], [], []], [['green', 'blue'], [], [], []], [[], [], [], []]]]
        self.door_lock_lst = [[[[False], [], [], []], [[True, True], [], [], []], [[], [], [], []]]]
        self.room_objects = [[[],['key'],['box']]]
        self.room_objects_color = [[[], ['blue'], ['yellow']]]
        super().__init__(
            num_rows=1,
            num_cols=3,
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

    # def reset(self, **kwargs):
    #     obs = super().reset(**kwargs)
    #
    #     # Recreate the verifier
    #     # self.instrs.reset_verifier(self)
    #
    #     # Compute the time step limit based on the maze size and instructions
    #     nav_time_room = self.room_size ** 2
    #     nav_time_maze = nav_time_room * self.num_rows * self.num_cols
    #     num_navs = self.num_navs_needed(self.instrs)
    #     self.max_steps = num_navs * nav_time_maze
    #
    #     return obs

    def gen_mission(self):
        # import pdb; pdb.set_trace()
        start_room = 1
        end_room = 2
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
                    self.add_object(c, r, kind=obj, color=self.room_objects_color[r][c][idx])
        self.place_agent(start_room,0)
        self.place_obj(Goal())
        # self.instrs = OpenInstr(ObjDesc('door', 'blue'), room=end_room)
        self.instrs = PickupInstr(ObjDesc('box'))


class Level_ThirdRoomGoalThreeRoomTest(RoomGridLevel):
    """
    Go to the red doorThree
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None, doors_per_side=3):
        self.doors_per_side=doors_per_side-1
        self.door_pos_lst = [[[[0], [], [], []],[[0,2], [], [], []], [[],[],[],[]]]]
        self.door_color_lst = [[[['red'], [], [], []], [['green', 'blue'], [], [], []], [[], [], [], []]]]
        self.door_lock_lst = [[[[False], [], [], []], [[True, True], [], [], []], [[], [], [], []]]]
        self.room_objects = [[[],[],[]]]
        self.room_objects_color = [[[], [], []]]
        super().__init__(
            num_rows=1,
            num_cols=3,
            room_size=5,
            seed=seed
        )

    def _gen_grid(self, width, height):
        #if deterministic goal :
        #self.put_obj(Goal(), width - 2, height - 2)
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

    # def reset(self, **kwargs):
    #     obs = super().reset(**kwargs)
    #
    #     # Recreate the verifier
    #     # self.instrs.reset_verifier(self)
    #
    #     # Compute the time step limit based on the maze size and instructions
    #     nav_time_room = self.room_size ** 2
    #     nav_time_maze = nav_time_room * self.num_rows * self.num_cols
    #     num_navs = self.num_navs_needed(self.instrs)
    #     self.max_steps = num_navs * nav_time_maze
    #
    #     return obs

    def restrict_to_room(self,room_restrict_lst):
        def restrict(env, pos):
            valid=True
            for room in room_restrict_lst:
                valid = valid and not env.room_grid[0][room].pos_inside(pos[0],pos[1])
            return valid
        return restrict

    def gen_mission(self):
        # import pdb; pdb.set_trace()
        start_room = 2
        end_room = 2
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
                    self.add_object(c, r, kind=obj, color=self.room_objects_color[r][c][idx])
        self.place_agent(start_room,0)
        #If stochastic goal      (for deterministic go to generate_grid)
        self.place_obj(Goal(), reject_fn = self.restrict_to_room([2]))
        # self.instrs = OpenInstr(ObjDesc('door', 'blue'), room=end_room)
        # self.instrs = PickupInstr(ObjDesc('box'))


class Level_GreenKeyGoalThreeRoomTest(RoomGridLevel):
    """
    Go to the red doorThree
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None, doors_per_side=3):
        self.doors_per_side=doors_per_side-1
        self.door_pos_lst = [[[[0], [], [], []],[[0,2], [], [], []], [[],[],[],[]]]]
        self.door_color_lst = [[[['red'], [], [], []], [['green', 'blue'], [], [], []], [[], [], [], []]]]
        self.door_lock_lst = [[[[False], [], [], []], [[True, True], [], [], []], [[], [], [], []]]]
        self.room_objects = [[[],['key'],[]]]
        self.room_objects_color = [[[], ['green'], []]]
        super().__init__(
            num_rows=1,
            num_cols=3,
            room_size=5,
            seed=seed
        )

    def _gen_grid(self, width, height):
        #if deterministic goal :
        #self.put_obj(Goal(), width - 2, height - 2)
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

    # def reset(self, **kwargs):
    #     obs = super().reset(**kwargs)
    #
    #     # Recreate the verifier
    #     # self.instrs.reset_verifier(self)
    #
    #     # Compute the time step limit based on the maze size and instructions
    #     nav_time_room = self.room_size ** 2
    #     nav_time_maze = nav_time_room * self.num_rows * self.num_cols
    #     num_navs = self.num_navs_needed(self.instrs)
    #     self.max_steps = num_navs * nav_time_maze
    #
    #     return obs

    def restrict_to_room(self,room_restrict_lst):
        def restrict(env, pos):
            valid=True
            for room in room_restrict_lst:
                valid = valid and not env.room_grid[0][room].pos_inside(pos[0],pos[1])
            return valid
        return restrict

    def gen_mission(self):
        # import pdb; pdb.set_trace()
        start_room = 0
        end_room = 2
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
                    self.add_object(c, r, kind=obj, color=self.room_objects_color[r][c][idx])
        self.place_agent(start_room,0)
        #If stochastic goal      (for deterministic go to generate_grid)
        self.place_obj(Goal(), reject_fn = self.restrict_to_room([2]))
        # self.instrs = OpenInstr(ObjDesc('door', 'blue'), room=end_room)
        self.instrs = PickupInstr(ObjDesc('box'))




class Level_GreenKeyGreenDoorFourRoomTest(RoomGridLevel):
    """
    Go to the red doorThree
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None, doors_per_side=3):
        self.doors_per_side=doors_per_side-1
        self.door_pos_lst = [[[[0], [], [], []],[[0,2], [], [], []], [[2],[],[],[]], [[],[],[],[]]]]
        self.door_color_lst = [[[['red'], [], [], []], [['green', 'blue'], [], [], []], [['yellow'], [], [], []], [[],[],[],[]]]]
        self.door_lock_lst = [[[[False], [], [], []], [[True, True], [], [], []], [[False], [], [], []], [[],[],[],[]]]]
        self.room_objects = [[[],['key'],[],[]]]
        self.room_objects_color = [[[], ['green'], [], []]]
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

    # def reset(self, **kwargs):
    #     obs = super().reset(**kwargs)
    #
    #     # Recreate the verifier
    #     # self.instrs.reset_verifier(self)
    #
    #     # Compute the time step limit based on the maze size and instructions
    #     nav_time_room = self.room_size ** 2
    #     nav_time_maze = nav_time_room * self.num_rows * self.num_cols
    #     num_navs = self.num_navs_needed(self.instrs)
    #     self.max_steps = num_navs * nav_time_maze
    #
    #     return obs

    def gen_mission(self):
        # import pdb; pdb.set_trace()
        start_room = 1
        end_room = 2
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
                    self.add_object(c, r, kind=obj, color=self.room_objects_color[r][c][idx])
        self.place_agent(start_room,0)
        self.instrs = OpenInstr(ObjDesc('door', 'green'), room=end_room)



class Level_BlueKeyBlueDoorFourRoomTest(RoomGridLevel):
    """
    Go to the red doorThree
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None, doors_per_side=3):
        self.doors_per_side=doors_per_side-1
        self.door_pos_lst = [[[[0], [], [], []],[[0,2], [], [], []], [[2],[],[],[]], [[],[],[],[]]]]
        self.door_color_lst = [[[['red'], [], [], []], [['green', 'blue'], [], [], []], [['yellow'], [], [], []], [[],[],[],[]]]]
        self.door_lock_lst = [[[[False], [], [], []], [[True, True], [], [], []], [[False], [], [], []], [[],[],[],[]]]]
        self.room_objects = [[[],['key'],[],[]]]
        self.room_objects_color = [[[], ['blue'], [], []]]
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

    # def reset(self, **kwargs):
    #     obs = super().reset(**kwargs)
    #
    #     # Recreate the verifier
    #     # self.instrs.reset_verifier(self)
    #
    #     # Compute the time step limit based on the maze size and instructions
    #     nav_time_room = self.room_size ** 2
    #     nav_time_maze = nav_time_room * self.num_rows * self.num_cols
    #     num_navs = self.num_navs_needed(self.instrs)
    #     self.max_steps = num_navs * nav_time_maze
    #
    #     return obs

    def gen_mission(self):
        # import pdb; pdb.set_trace()
        start_room = 1
        end_room = 2
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
                    self.add_object(c, r, kind=obj, color=self.room_objects_color[r][c][idx])
        self.place_agent(start_room,0)
        self.instrs = OpenInstr(ObjDesc('door', 'blue'), room=end_room)





class Level_Rm2DoorBC(RoomGridLevel):
    """
    Go to the red door
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None):
        super().__init__(
            num_rows=1,
            num_cols=2,
            room_size=9,
            seed=seed
        )

    def gen_mission(self):
        #import pdb; pdb.set_trace()
        obj1, _ = self.add_door(0, 0,0,  'blue', locked=False, door_loc_y=0)
        obj2, _ = self.add_door(0, 0,0,  'yellow', locked=False, door_loc_y=1)
        self.place_agent(0, 0)
        self.instrs = OpenInstr(ObjDesc('door', 'red'))

    class Level_Rm3DoorD(RoomGridLevel):
        """
        Go to the red door
        (always unlocked, in the current room)
        Note: this level is intentionally meant for debugging and is
        intentionally kept very simple.
        """

        def __init__(self, seed=None):
            super().__init__(
                num_rows=1,
                num_cols=2,
                room_size=9,
                seed=seed
            )

        def gen_mission(self):
            #import pdb; pdb.set_trace()
            obj, _ = self.add_door(0, 0,0,  'green', locked=False, door_loc_y=0)
            self.place_agent(0, 0)
            self.instrs = OpenInstr(ObjDesc('door', 'red'))

class Level_GoToRedBlueBall(RoomGridLevel):
    """
    Go to the red ball or to the blue ball.
    There is exactly one red or blue ball, and some distractors.
    The distractors are guaranteed not to be red or blue balls.
    Language is not required to solve this level.
    """

    def __init__(self, room_size=8, num_dists=7, seed=None):
        self.num_dists = num_dists
        super().__init__(
            num_rows=1,
            num_cols=1,
            room_size=room_size,
            seed=seed
        )

    def gen_mission(self):
        self.place_agent()

        dists = self.add_distractors(num_distractors=self.num_dists, all_unique=False)

        # Ensure there is only one red or blue ball
        for dist in dists:
            if dist.type == 'ball' and (dist.color == 'blue' or dist.color == 'red'):
                raise RejectSampling('can only have one blue or red ball')

        color = self._rand_elem(['red', 'blue'])
        obj, _ = self.add_object(0, 0, 'ball', color)

        # Make sure no unblocking is required
        self.check_objs_reachable()

        self.instrs = GoToInstr(ObjDesc(obj.type, obj.color))


class Level_OpenRedDoor(RoomGridLevel):
    """
    Go to the red door
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None):
        super().__init__(
            num_rows=1,
            num_cols=2,
            room_size=5,
            seed=seed
        )

    def gen_mission(self):
        obj, _ = self.add_door(0, 0, 0, 'red', locked=False)
        self.place_agent(0, 0)
        self.instrs = OpenInstr(ObjDesc('door', 'red'))


class Level_OpenDoor(RoomGridLevel):
    """
    Go to the door
    The door to open is given by its color or by its location.
    (always unlocked, in the current room)
    """

    def __init__(
        self,
        debug=False,
        select_by=None,
        seed=None
    ):
        self.select_by = select_by
        self.debug = debug
        super().__init__(seed=seed)

    def gen_mission(self):
        door_colors = self._rand_subset(COLOR_NAMES, 4)
        objs = []

        for i, color in enumerate(door_colors):
            obj, _ = self.add_door(1, 1, door_idx=i, color=color, locked=False)
            objs.append(obj)

        select_by = self.select_by
        if select_by is None:
            select_by = self._rand_elem(["color", "loc"])
        if select_by == "color":
            object = ObjDesc(objs[0].type, color=objs[0].color)
        elif select_by == "loc":
            object = ObjDesc(objs[0].type, loc=self._rand_elem(LOC_NAMES))

        self.place_agent(1, 1)
        self.instrs = OpenInstr(object, strict=self.debug)


class Level_OpenDoorDebug(Level_OpenDoor):
    """
    Same as OpenDoor but the level stops when any door is opened
    """

    def __init__(
        self,
        select_by=None,
        seed=None
    ):
        super().__init__(select_by=select_by, debug=True, seed=seed)


class Level_OpenDoorColor(Level_OpenDoor):
    """
    Go to the door
    The door is selected by color.
    (always unlocked, in the current room)
    """

    def __init__(self, seed=None):
        super().__init__(
            select_by="color",
            seed=seed
        )


#class Level_OpenDoorColorDebug(Level_OpenDoorColor, Level_OpenDoorDebug):
    """
    Same as OpenDoorColor but the level stops when any door is opened
    """
#    pass


class Level_OpenDoorLoc(Level_OpenDoor):
    """
    Go to the door
    The door is selected by location.
    (always unlocked, in the current room)
    """

    def __init__(self, seed=None):
        super().__init__(
            select_by="loc",
            seed=seed
        )


class Level_GoToDoor(RoomGridLevel):
    """
    Go to a door
    (of a given color, in the current room)
    No distractors, no language variation
    """

    def __init__(self, seed=None):
        super().__init__(
            room_size=7,
            seed=seed
        )

    def gen_mission(self):
        objs = []
        for _ in range(4):
            door, _ = self.add_door(1, 1)
            objs.append(door)
        self.place_agent(1, 1)

        obj = self._rand_elem(objs)
        self.instrs = GoToInstr(ObjDesc('door', obj.color))


class Level_GoToObjDoor(RoomGridLevel):
    """
    Go to an object or door
    (of a given type and color, in the current room)
    """

    def __init__(self, seed=None):
        super().__init__(
            room_size=8,
            seed=seed
        )

    def gen_mission(self):
        self.place_agent(1, 1)
        objs = self.add_distractors(1, 1, num_distractors=8, all_unique=False)

        for _ in range(4):
            door, _ = self.add_door(1, 1)
            objs.append(door)

        self.check_objs_reachable()

        obj = self._rand_elem(objs)
        self.instrs = GoToInstr(ObjDesc(obj.type, obj.color))


class Level_ActionObjDoor(RoomGridLevel):
    """
    [pick up an object] or
    [go to an object or door] or
    [open a door]
    (in the current room)
    """

    def __init__(self, seed=None):
        super().__init__(
            room_size=7,
            seed=seed
        )

    def gen_mission(self):
        objs = self.add_distractors(1, 1, num_distractors=5)
        for _ in range(4):
            door, _ = self.add_door(1, 1, locked=False)
            objs.append(door)

        self.place_agent(1, 1)

        obj = self._rand_elem(objs)
        desc = ObjDesc(obj.type, obj.color)

        if obj.type == 'door':
            if self._rand_bool():
                self.instrs = GoToInstr(desc)
            else:
                self.instrs = OpenInstr(desc)
        else:
            if self._rand_bool():
                self.instrs = GoToInstr(desc)
            else:
                self.instrs = PickupInstr(desc)


class Level_UnlockLocal(RoomGridLevel):
    """
    Fetch a key and unlock a door
    (in the current room)
    """

    def __init__(self, distractors=False, seed=None):
        self.distractors = distractors
        super().__init__(seed=seed)

    def gen_mission(self):
        door, _ = self.add_door(1, 1, locked=True)
        self.add_object(1, 1, 'key', door.color)
        if self.distractors:
            self.add_distractors(1, 1, num_distractors=3)
        self.place_agent(1, 1)

        self.instrs = OpenInstr(ObjDesc(door.type))


class Level_UnlockLocalDist(Level_UnlockLocal):
    """
    Fetch a key and unlock a door
    (in the current room, with distractors)
    """

    def __init__(self, seed=None):
        super().__init__(distractors=True, seed=seed)


class Level_KeyInBox(RoomGridLevel):
    """
    Unlock a door. Key is in a box (in the current room).
    """

    def __init__(self, seed=None):
        super().__init__(
            seed=seed
        )

    def gen_mission(self):
        door, _ = self.add_door(1, 1, locked=True)

        # Put the key in the box, then place the box in the room
        key = Key(door.color)
        box = Box(self._rand_color(), key)
        self.place_in_room(1, 1, box)

        self.place_agent(1, 1)

        self.instrs = OpenInstr(ObjDesc(door.type))


class Level_UnlockPickup(RoomGridLevel):
    """
    Unlock a door, then pick up a box in another room
    """

    def __init__(self, distractors=False, seed=None):
        self.distractors = distractors

        room_size = 6
        super().__init__(
            num_rows=1,
            num_cols=2,
            room_size=room_size,
            max_steps=8*room_size**2,
            seed=seed
        )

    def gen_mission(self):
        # Add a random object to the room on the right
        obj, _ = self.add_object(1, 0, kind="box")
        # Make sure the two rooms are directly connected by a locked door
        door, _ = self.add_door(0, 0, 0, locked=True)
        # Add a key to unlock the door
        self.add_object(0, 0, 'key', door.color)
        if self.distractors:
            self.add_distractors(num_distractors=4)

        self.place_agent(0, 0)

        self.instrs = PickupInstr(ObjDesc(obj.type, obj.color))


class Level_UnlockPickupDist(Level_UnlockPickup):
    """
    Unlock a door, then pick up an object in another room
    (with distractors)
    """

    def __init__(self, seed=None):
        super().__init__(distractors=True, seed=seed)


class Level_BlockedUnlockPickup(RoomGridLevel):
    """
    Unlock a door blocked by a ball, then pick up a box
    in another room
    """

    def __init__(self, seed=None):
        room_size = 6
        super().__init__(
            num_rows=1,
            num_cols=2,
            room_size=room_size,
            max_steps=16*room_size**2,
            seed=seed
        )

    def gen_mission(self):
        # Add a box to the room on the right
        obj, _ = self.add_object(1, 0, kind="box")
        # Make sure the two rooms are directly connected by a locked door
        door, pos = self.add_door(0, 0, 0, locked=True)
        # Block the door with a ball
        color = self._rand_color()
        self.grid.set(pos[0]-1, pos[1], Ball(color))
        # Add a key to unlock the door
        self.add_object(0, 0, 'key', door.color)

        self.place_agent(0, 0)

        self.instrs = PickupInstr(ObjDesc(obj.type))


class Level_UnlockToUnlock(RoomGridLevel):
    """
    Unlock a door A that requires to unlock a door B before
    """

    def __init__(self, seed=None):
        room_size = 6
        super().__init__(
            num_rows=1,
            num_cols=3,
            room_size=room_size,
            max_steps=30*room_size**2,
            seed=seed
        )

    def gen_mission(self):
        colors = self._rand_subset(COLOR_NAMES, 2)

        # Add a door of color A connecting left and middle room
        self.add_door(0, 0, door_idx=0, color=colors[0], locked=True)

        # Add a key of color A in the room on the right
        self.add_object(2, 0, kind="key", color=colors[0])

        # Add a door of color B connecting middle and right room
        self.add_door(1, 0, door_idx=0, color=colors[1], locked=True)

        # Add a key of color B in the middle room
        self.add_object(1, 0, kind="key", color=colors[1])

        obj, _ = self.add_object(0, 0, kind="ball")

        self.place_agent(1, 0)

        self.instrs = PickupInstr(ObjDesc(obj.type))


class Level_PickupDist(RoomGridLevel):
    """
    Pick up an object
    The object to pick up is given by its type only, or
    by its color, or by its type and color.
    (in the current room, with distractors)
    """

    def __init__(self, debug=False, seed=None):
        self.debug = debug
        super().__init__(
            num_rows = 1,
            num_cols = 1,
            room_size=7,
            seed=seed
        )

    def gen_mission(self):
        # Add 5 random objects in the room
        objs = self.add_distractors(num_distractors=5)
        self.place_agent(0, 0)
        obj = self._rand_elem(objs)
        type = obj.type
        color = obj.color

        select_by = self._rand_elem(["type", "color", "both"])
        if select_by == "color":
            type = None
        elif select_by == "type":
            color = None

        self.instrs = PickupInstr(ObjDesc(type, color), strict=self.debug)


class Level_PickupDistDebug(Level_PickupDist):
    """
    Same as PickupDist but the level stops when any object is picked
    """

    def __init__(self, seed=None):
        super().__init__(
            debug=True,
            seed=seed
        )


class Level_PickupAbove(RoomGridLevel):
    """
    Pick up an object (in the room above)
    This task requires to use the compass to be solved effectively.
    """

    def __init__(self, seed=None):
        room_size = 6
        super().__init__(
            room_size=room_size,
            max_steps=8*room_size**2,
            seed=seed
        )

    def gen_mission(self):
        # Add a random object to the top-middle room
        obj, pos = self.add_object(1, 0)
        # Make sure the two rooms are directly connected
        self.add_door(1, 1, 3, locked=False)
        self.place_agent(1, 1)
        self.connect_all()

        self.instrs = PickupInstr(ObjDesc(obj.type, obj.color))


class Level_OpenTwoDoors(RoomGridLevel):
    """
    Open door X, then open door Y
    The two doors are facing opposite directions, so that the agent
    Can't see whether the door behind him is open.
    This task requires memory (recurrent policy) to be solved effectively.
    """

    def __init__(self,
        first_color=None,
        second_color=None,
        strict=False,
        seed=None
    ):
        self.first_color = first_color
        self.second_color = second_color
        self.strict = strict

        room_size = 6
        super().__init__(
            room_size=room_size,
            max_steps=20*room_size**2,
            seed=seed
        )

    def gen_mission(self):
        colors = self._rand_subset(COLOR_NAMES, 2)

        first_color = self.first_color
        if first_color is None:
            first_color = colors[0]
        second_color = self.second_color
        if second_color is None:
            second_color = colors[1]

        door1, _ = self.add_door(1, 1, 2, color=first_color, locked=False)
        door2, _ = self.add_door(1, 1, 0, color=second_color, locked=False)

        self.place_agent(1, 1)

        self.instrs = BeforeInstr(
            OpenInstr(ObjDesc(door1.type, door1.color), strict=self.strict),
            OpenInstr(ObjDesc(door2.type, door2.color))
        )


class Level_OpenTwoDoorsDebug(Level_OpenTwoDoors):
    """
    Same as OpenTwoDoors but the level stops when the second door is opened
    """

    def __init__(self,
        first_color=None,
        second_color=None,
        seed=None
    ):
        super().__init__(
            first_color,
            second_color,
            strict=True,
            seed=seed
        )


class Level_OpenRedBlueDoors(Level_OpenTwoDoors):
    """
    Open red door, then open blue door
    The two doors are facing opposite directions, so that the agent
    Can't see whether the door behind him is open.
    This task requires memory (recurrent policy) to be solved effectively.
    """

    def __init__(self, seed=None):
        super().__init__(
            first_color="red",
            second_color="blue",
            seed=seed
        )


class Level_OpenRedBlueDoorsDebug(Level_OpenTwoDoorsDebug):
    """
    Same as OpenRedBlueDoors but the level stops when the blue door is opened
    """

    def __init__(self, seed=None):
        super().__init__(
            first_color="red",
            second_color="blue",
            seed=seed
        )


class Level_FindObjS5(RoomGridLevel):
    """
    Pick up an object (in a random room)
    Rooms have a size of 5
    This level requires potentially exhaustive exploration
    """

    def __init__(self, room_size=5, seed=None):
        super().__init__(
            room_size=room_size,
            max_steps=20*room_size**2,
            seed=seed
        )

    def gen_mission(self):
        # Add a random object to a random room
        i = self._rand_int(0, self.num_rows)
        j = self._rand_int(0, self.num_cols)
        obj, _ = self.add_object(i, j)
        self.place_agent(1, 1)
        self.connect_all()
        print('THIS IS THE : ' ,type(obj.type))
        self.instrs = PickupInstr(ObjDesc(obj.type))


class Level_FindObjS6(Level_FindObjS5):
    """
    Same as the FindObjS5 level, but rooms have a size of 6
    """

    def __init__(self, seed=None):
        super().__init__(
            room_size=6,
            seed=seed
        )


class Level_FindObjS7(Level_FindObjS5):
    """
    Same as the FindObjS5 level, but rooms have a size of 7
    """

    def __init__(self, seed=None):
        super().__init__(
            room_size=7,
            seed=seed
        )


class KeyCorridor(RoomGridLevel):
    """
    A ball is behind a locked door, the key is placed in a
    random room.
    """

    def __init__(
        self,
        num_rows=3,
        obj_type="ball",
        room_size=6,
        seed=None
    ):
        self.obj_type = obj_type

        super().__init__(
            room_size=room_size,
            num_rows=num_rows,
            max_steps=30*room_size**2,
            seed=seed,
        )

    def gen_mission(self):
        # Connect the middle column rooms into a hallway
        for j in range(1, self.num_rows):
            self.remove_wall(1, j, 3)

        # Add a locked door on the bottom right
        # Add an object behind the locked door
        room_idx = self._rand_int(0, self.num_rows)
        door, _ = self.add_door(2, room_idx, 2, locked=True)
        obj, _ = self.add_object(2, room_idx, kind=self.obj_type)

        # Add a key in a random room on the left side
        self.add_object(0, self._rand_int(0, self.num_rows), 'key', door.color)

        # Place the agent in the middle
        self.place_agent(1, self.num_rows // 2)

        # Make sure all rooms are accessible
        self.connect_all()

        self.instrs = PickupInstr(ObjDesc(obj.type))


class Level_KeyCorridorS3R1(KeyCorridor):
    def __init__(self, seed=None):
        super().__init__(
            room_size=3,
            num_rows=1,
            seed=seed
        )

class Level_KeyCorridorS3R2(KeyCorridor):
    def __init__(self, seed=None):
        super().__init__(
            room_size=3,
            num_rows=2,
            seed=seed
        )

class Level_KeyCorridorS3R3(KeyCorridor):
    def __init__(self, seed=None):
        super().__init__(
            room_size=3,
            num_rows=3,
            seed=seed
        )

class Level_KeyCorridorS4R3(KeyCorridor):
    def __init__(self, seed=None):
        super().__init__(
            room_size=4,
            num_rows=3,
            seed=seed
        )

class Level_KeyCorridorS5R3(KeyCorridor):
    def __init__(self, seed=None):
        super().__init__(
            room_size=5,
            num_rows=3,
            seed=seed
        )

class Level_KeyCorridorS6R3(KeyCorridor):
    def __init__(self, seed=None):
        super().__init__(
            room_size=6,
            num_rows=3,
            seed=seed
        )

####################################################
class Level_OpenOneDoor(RoomGridLevel):
    """
    Go to the sole door
    (always unlocked, in the current room)
    Note: this level is intentionally meant for debugging and is
    intentionally kept very simple.
    """

    def __init__(self, seed=None):
        super().__init__(
            num_rows=1,
            num_cols=2,
            room_size=5,
            seed=seed
        )

    def gen_mission(self):
        obj, _ = self.add_door(0, 0, 0, locked=False)
        self.place_agent()
        self.instrs = OpenInstr(ObjDesc('door'))
####################################################

####################################################
class Level_PickupKey(RoomGridLevel):
    """
    Pick up the key
    Rooms have a size of 6
    """

    def __init__(self, room_size=8, seed=None):
        super().__init__(
            room_size=room_size,
            num_rows=1,
            num_cols=1,
            seed=seed
        )

    def gen_mission(self):
        obj, _ = self.add_object(0, 0, kind="key")
        self.place_agent()
        self.instrs = PickupInstr(ObjDesc(obj.type))
####################################################

class Level_1RoomS8(RoomGridLevel):
    """
    Pick up the ball
    Rooms have a size of 8
    """

    def __init__(self, room_size=8, seed=None):
        super().__init__(
            room_size=room_size,
            num_rows=1,
            num_cols=1,
            seed=seed
        )

    def gen_mission(self):
        obj, _ = self.add_object(0, 0, kind="ball")
        self.place_agent()
        self.instrs = PickupInstr(ObjDesc(obj.type))


class Level_1RoomS12(Level_1RoomS8):
    """
    Pick up the ball
    Rooms have a size of 12
    """

    def __init__(self, seed=None):
        super().__init__(
            room_size=12,
            seed=seed
        )


class Level_1RoomS16(Level_1RoomS8):
    """
    Pick up the ball
    Rooms have a size of 16
    """

    def __init__(self, seed=None):
        super().__init__(
            room_size=16,
            seed=seed
        )


class Level_1RoomS20(Level_1RoomS8):
    """
    Pick up the ball
    Rooms have a size of 20
    """

    def __init__(self, seed=None):
        super().__init__(
            room_size=20,
            seed=seed
        )


class PutNext(RoomGridLevel):
    """
    Task of the form: move the A next to the B and the C next to the D.
    This task is structured to have a very large number of possible
    instructions.
    """

    def __init__(
        self,
        room_size,
        objs_per_room,
        start_carrying=False,
        seed=None
    ):
        assert room_size >= 4
        assert objs_per_room <= 9
        self.objs_per_room = objs_per_room
        self.start_carrying = start_carrying

        super().__init__(
            num_rows=1,
            num_cols=2,
            room_size=room_size,
            max_steps=8*room_size**2,
            seed=seed
        )

    def gen_mission(self):
        self.place_agent(0, 0)

        # Add objects to both the left and right rooms
        # so that we know that we have two non-adjacent set of objects
        objs_l = self.add_distractors(0, 0, self.objs_per_room)
        objs_r = self.add_distractors(1, 0, self.objs_per_room)

        # Remove the wall between the two rooms
        self.remove_wall(0, 0, 0)

        # Select objects from both subsets
        a = self._rand_elem(objs_l)
        b = self._rand_elem(objs_r)

        # Randomly flip the object to be moved
        if self._rand_bool():
            t = a
            a = b
            b = t

        self.obj_a = a

        self.instrs = PutNextInstr(
            ObjDesc(a.type, a.color),
            ObjDesc(b.type, b.color)
        )

    def reset(self, **kwargs):
        obs = super().reset(**kwargs)

        # If the agent starts off carrying the object
        if self.start_carrying:
            self.grid.set(*self.obj_a.init_pos, None)
            self.carrying = self.obj_a

        return obs


class Level_PutNextS4N1(PutNext):
    def __init__(self, seed=None):
        super().__init__(
            room_size=4,
            objs_per_room=1,
            seed=seed
        )


class Level_PutNextS5N1(PutNext):
    def __init__(self, seed=None):
        super().__init__(
            room_size=5,
            objs_per_room=1,
            seed=seed
        )


class Level_PutNextS5N2(PutNext):
    def __init__(self, seed=None):
        super().__init__(
            room_size=5,
            objs_per_room=2,
            seed=seed
        )


class Level_PutNextS6N3(PutNext):
    def __init__(self, seed=None):
        super().__init__(
            room_size=6,
            objs_per_room=3,
            seed=seed
        )


class Level_PutNextS7N4(PutNext):
    def __init__(self, seed=None):
        super().__init__(
            room_size=7,
            objs_per_room=4,
            seed=seed
        )


class Level_PutNextS5N2Carrying(PutNext):
    def __init__(self, seed=None):
        super().__init__(
            room_size=5,
            objs_per_room=2,
            start_carrying=True,
            seed=seed
        )


class Level_PutNextS6N3Carrying(PutNext):
    def __init__(self, seed=None):
        super().__init__(
            room_size=6,
            objs_per_room=3,
            start_carrying=True,
            seed=seed
        )


class Level_PutNextS7N4Carrying(PutNext):
    def __init__(self, seed=None):
        super().__init__(
            room_size=7,
            objs_per_room=4,
            start_carrying=True,
            seed=seed
        )


class MoveTwoAcross(RoomGridLevel):
    """
    Task of the form: move the A next to the B and the C next to the D.
    This task is structured to have a very large number of possible
    instructions.
    """

    def __init__(
        self,
        room_size,
        objs_per_room,
        seed=None
    ):
        assert objs_per_room <= 9
        self.objs_per_room = objs_per_room

        super().__init__(
            num_rows=1,
            num_cols=2,
            room_size=room_size,
            max_steps=16*room_size**2,
            seed=seed
        )

    def gen_mission(self):
        self.place_agent(0, 0)

        # Add objects to both the left and right rooms
        # so that we know that we have two non-adjacent set of objects
        objs_l = self.add_distractors(0, 0, self.objs_per_room)
        objs_r = self.add_distractors(1, 0, self.objs_per_room)

        # Remove the wall between the two rooms
        self.remove_wall(0, 0, 0)

        # Select objects from both subsets
        objs_l = self._rand_subset(objs_l, 2)
        objs_r = self._rand_subset(objs_r, 2)
        a = objs_l[0]
        b = objs_r[0]
        c = objs_r[1]
        d = objs_l[1]

        self.instrs = BeforeInstr(
            PutNextInstr(ObjDesc(a.type, a.color), ObjDesc(b.type, b.color)),
            PutNextInstr(ObjDesc(c.type, c.color), ObjDesc(d.type, d.color))
        )


class Level_MoveTwoAcrossS5N2(MoveTwoAcross):
    def __init__(self, seed=None):
        super().__init__(
            room_size=5,
            objs_per_room=2,
            seed=seed
        )


class Level_MoveTwoAcrossS8N9(MoveTwoAcross):
    def __init__(self, seed=None):
        super().__init__(
            room_size=8,
            objs_per_room=9,
            seed=seed
        )


class OpenDoorsOrder(RoomGridLevel):
    """
    Open one or two doors in the order specified.
    """

    def __init__(
        self,
        num_doors,
        debug=False,
        seed=None
    ):
        assert num_doors >= 2
        self.num_doors = num_doors
        self.debug = debug

        room_size = 6
        super().__init__(
            room_size=room_size,
            max_steps=20*room_size**2,
            seed=seed
        )

    def gen_mission(self):
        colors = self._rand_subset(COLOR_NAMES, self.num_doors)
        doors = []
        for i in range(self.num_doors):
            door, _ = self.add_door(1, 1, color=colors[i], locked=False)
            doors.append(door)
        self.place_agent(1, 1)

        door1, door2 = self._rand_subset(doors, 2)
        desc1 = ObjDesc(door1.type, door1.color)
        desc2 = ObjDesc(door2.type, door2.color)

        mode = self._rand_int(0, 3)
        if mode == 0:
            self.instrs = OpenInstr(desc1, strict=self.debug)
        elif mode == 1:
            self.instrs = BeforeInstr(OpenInstr(desc1, strict=self.debug), OpenInstr(desc2, strict=self.debug))
        elif mode == 2:
            self.instrs = AfterInstr(OpenInstr(desc1, strict=self.debug), OpenInstr(desc2, strict=self.debug))
        else:
            assert False

class Level_OpenDoorsOrderN2(OpenDoorsOrder):
    def __init__(self, seed=None):
        super().__init__(
            num_doors=2,
            seed=seed
        )


class Level_OpenDoorsOrderN4(OpenDoorsOrder):
    def __init__(self, seed=None):
        super().__init__(
            num_doors=4,
            seed=seed
        )


class Level_OpenDoorsOrderN2Debug(OpenDoorsOrder):
    def __init__(self, seed=None):
        super().__init__(
            num_doors=2,
            debug=True,
            seed=seed
        )


class Level_OpenDoorsOrderN4Debug(OpenDoorsOrder):
    def __init__(self, seed=None):
        super().__init__(
            num_doors=4,
            debug=True,
            seed=seed
        )


for name, level in list(globals().items()):
    if name.startswith('Level_'):
        level.is_bonus = True


# Register the levels in this file
register_levels(__name__, globals())
