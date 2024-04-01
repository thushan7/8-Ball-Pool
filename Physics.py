import phylib;
import sqlite3;
import os;
import math;

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";
FOOTER = """</svg>\n""";
FRAME_INTERVAL = 0.01; #one frame every 0.01 seconds
################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;
HOLE_RADIUS   = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH  = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH   = phylib.PHYLIB_TABLE_WIDTH;
SIM_RATE      = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON   = phylib.PHYLIB_VEL_EPSILON;
DRAG          = phylib.PHYLIB_DRAG;
MAX_TIME      = phylib.PHYLIB_MAX_TIME;
MAX_OBJECTS   = phylib.PHYLIB_MAX_OBJECTS;
################################################################################
BALL_COLOURS = [
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",
    "MEDIUMPURPLE",
    "LIGHTSALMON",
    "LIGHTGREEN",
    "SANDYBROWN",
    ];
################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self,
                                       phylib.PHYLIB_STILL_BALL,
                                       number,
                                       pos, None, None,
                                       0.0, 0.0 );

        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;


    def svg( self ):
        """
        SVG function.
        """
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number]);


################################################################################
class RollingBall( phylib.phylib_object ):
    """
    Python RollingBall class.
    """

    def __init__( self, number, pos, vel, acc ):
        """
	    Constructor function. Requires ball number as well as position,
	    velocity, and acceleration in (x,y) form as arguments.
	    """

        phylib.phylib_object.__init__( self,
                                       phylib.PHYLIB_ROLLING_BALL,
                                       number, pos, vel, acc, 0.0, 0.0);
        self.__class__ = RollingBall;


    def svg( self ):
        """
        SVG function.
        """
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number]);


################################################################################
class Hole( phylib.phylib_object ):
    """
    Python Hole class.
    """

    def __init__(self, pos ):
        """
	    Constructor function. Requires hole position as argument.
	    """

        phylib.phylib_object.__init__( self,
			                           phylib.PHYLIB_HOLE,
			                           0, pos, None, None, 0.0, 0.0);
        self.__class__ = Hole;


    def svg( self ):
        """
        SVG function.
        """
        return """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS);


################################################################################
class HCushion( phylib.phylib_object ):
    """
    Python HCushion class.
    """

    def __init__( self, y ):
        """
	    Constructor function. Requires cushion's y-coord as argument.
	    """

        phylib.phylib_object.__init__( self,
				                       phylib.PHYLIB_HCUSHION,
			                           0, None, None, None, None, y);
        self.__class__ = HCushion;


    def svg( self ):
        """
        SVG function.
        """
        if (self.obj.hcushion.y == 0):
            return """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (-25);
        else:
            return """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (2700);


################################################################################
class VCushion( phylib.phylib_object ):
    """
    Python VCushion class.
    """

    def __init__( self, x ):
        """
        Constructor function. Requires cushion's x-coord as argument.
        """

        phylib.phylib_object.__init__( self,
                                       phylib.PHYLIB_VCUSHION,
                                       0, None, None, None, x, None);
        self.__class__ = VCushion;


    def svg( self ):
        """
        SVG function.
        """
        if (self.obj.vcushion.x == 0):
            return """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (-25);
        else:
            return """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (1350);


################################################################################
class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index );
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    def svg( self ):
        """
        SVG function.
        """
        string = HEADER;
        for obj in self:
            if obj is not None:
                string += obj.svg();
        string += FOOTER;
        return string;

    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                #create new ball with same number as old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                       Coordinate(0,0),
                                       Coordinate(0,0),
                                       Coordinate(0,0) );
                #compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );

                #add ball to table
                new += new_ball;

            if isinstance( ball, StillBall ):
                #create new ball with same number and pos as old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                                     Coordinate( ball.obj.still_ball.pos.x,
                                                ball.obj.still_ball.pos.y) );
                #add ball to table
                new += new_ball;

        return new;


################################################################################
class Database():
    """
    Database class.
    """

    conn = None; #database connection

    def __init__( self, reset=False ):
        """
        This function initializes the database.
        If reset is set to True, any existing database is deleted and a new one is created.
        """

        if reset and os.path.exists("phylib.db"):
            os.remove("phylib.db");
        Database.conn = sqlite3.connect("phylib.db");

    def createDB( self ):
        """
        This function creates the tables of the database if they don't exist already.
        """

        cursor = Database.conn.cursor();
        cursor.execute("""CREATE TABLE IF NOT EXISTS Ball (BALLID INTEGER NOT NULL, BALLNO INTEGER NOT NULL, XPOS FLOAT NOT NULL, YPOS FLOAT NOT NULL, XVEL FLOAT, YVEL FLOAT, PRIMARY KEY (BALLID))""");
        cursor.execute("""CREATE TABLE IF NOT EXISTS TTable (TABLEID INTEGER NOT NULL, TIME FLOAT NOT NULL, PRIMARY KEY (TABLEID))""");
        cursor.execute("""CREATE TABLE IF NOT EXISTS BallTable (BALLID INTEGER NOT NULL, TABLEID INTEGER NOT NULL, FOREIGN KEY (BALLID) REFERENCES Ball(BALLID), FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID))""");
        cursor.execute("""CREATE TABLE IF NOT EXISTS Shot (SHOTID INTEGER NOT NULL, PLAYERID INTEGER NOT NULL, GAMEID INTEGER NOT NULL, PRIMARY KEY (SHOTID), FOREIGN KEY (PLAYERID) REFERENCES Player(PLAYERID), FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID))""");
        cursor.execute("""CREATE TABLE IF NOT EXISTS TableShot (TABLEID INTEGER NOT NULL, SHOTID INTEGER NOT NULL, FOREIGN KEY (TABLEID) REFERENCES TTable, FOREIGN KEY (SHOTID) REFERENCES Shot(SHOTID))""");
        cursor.execute("""CREATE TABLE IF NOT EXISTS Game (GAMEID INTEGER NOT NULL, GAMENAME VARCHAR(64) NOT NULL, PRIMARY KEY (GAMEID))""");
        cursor.execute("""CREATE TABLE IF NOT EXISTS Player (PLAYERID INTEGER NOT NULL, GAMEID INTEGER NOT NULL, PLAYERNAME VARCHAR(64) NOT NULL, PRIMARY KEY (PLAYERID), FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID))""");
        cursor.close();
        Database.conn.commit();

    def readTable( self, tableID ):
        """
        This function reads a Table object from the database based on a given tableID.
        """

        cursor = Database.conn.cursor();

        #do nothing and exit function if the tableID doesn't exist in the database
        cursor.execute("""SELECT *
                                FROM BallTable
                                WHERE BallTable.TABLEID=?""", (tableID+1,));
        tablePresent = cursor.fetchall();
        if not tablePresent:
            cursor.close();
            Database.conn.commit();
            return None;
    
        table = Table();

        #retrieve data on all balls on table
        cursor.execute("""SELECT * 
                                FROM Ball
                                INNER JOIN BallTable ON Ball.BALLID=BallTable.BALLID
                                WHERE BallTable.TABLEID=?""", (tableID+1,));
        balls = cursor.fetchall();

        #create all ball objects and add them to the table
        for ball in balls:
            ballID, ballNo, xPos, yPos, xVel, yVel, xAcc, yAcc = ball;
            if xVel is None and yVel is None:
                newBall = StillBall(ballNo, Coordinate(xPos, yPos));
            else:
                speed = math.sqrt(xVel**2 + yVel**2);
                xAcc = 0;
                yAcc = 0;
                if (speed > VEL_EPSILON):
                    xAcc = (-1)*(xVel)/speed*DRAG;
                    yAcc = (-1)*(yVel)/speed*DRAG;
                newBall = RollingBall(ballNo, Coordinate(xPos, yPos), 
                                                Coordinate(xVel, yVel),
                                                Coordinate(xAcc, yAcc));
            table += newBall;
            
        #update time parameter for the table
        cursor.execute("""SELECT TIME
                                FROM TTable
                                WHERE TTable.TABLEID=?""", (tableID+1,));
        time = cursor.fetchone();
        table.time = time[0];
    
        cursor.close();
    
        return table;

    def writeTable( self, table ):
        """
        This table writes a table object into the database.
        """

        cursor = Database.conn.cursor();

        #update TTable with time for the table, retrieve tableID for the table
        cursor.execute("""INSERT
                                INTO TTable(TIME)
                                VALUES (?)""", (table.time,));
        tableID = cursor.lastrowid;

        #write all balls on table to the database
        for ball in table:
            if ball is not None:
                if isinstance(ball, StillBall) or isinstance(ball, RollingBall):
                    if isinstance(ball, StillBall):
                        cursor.execute("""INSERT
                                                INTO Ball(BALLNO, XPOS, YPOS)
                                                VALUES (?, ?, ?)""",
                                                (ball.obj.still_ball.number, ball.obj.still_ball.pos.x, ball.obj.still_ball.pos.y));
                    else:
                        cursor.execute("""INSERT
                                                INTO Ball(BALLNO, XPOS, YPOS, XVEL, YVEL)
                                                VALUES (?, ?, ?, ?, ?)""",
                                                (ball.obj.rolling_ball.number, ball.obj.rolling_ball.pos.x, ball.obj.rolling_ball.pos.y, ball.obj.rolling_ball.vel.x, ball.obj.rolling_ball.vel.y));
                    ballID = cursor.lastrowid;
                    cursor.execute("""INSERT
                                            INTO BallTable(BALLID, TABLEID)
                                            VALUES (?, ?)""",
                                            (ballID, tableID));
        
        cursor.close();
    
        return tableID-1;

    def close( self ):
        """
        This function commits and closes the database.
        """
        Database.conn.commit();
        Database.conn.close();


################################################################################
class Game():
    """
    Game class.
    """

    def __init__( self, gameID=None, gameName=None, player1Name=None, player2Name=None ):
        """
        This function initializes a Game based on what parameters are passed.
        """

        #create database
        self.db = Database();
        self.db.createDB();

        #creating game based on info in database using a given gameID
        if gameID is not None and isinstance(gameID, int) and gameName is None and player1Name is None and player2Name is None:
            cursor = Database.conn.cursor();

            #retrieve game name and player names from database, lower playerID becomes player1
            cursor.execute("""SELECT Game.GAMENAME, p1.PLAYERNAME, p2.PLAYERNAME
                                    FROM Game
                                    INNER JOIN Player AS p1 ON Game.GAMEID=p1.GAMEID
                                    INNER JOIN Player AS p2 ON Game.GAMEID=p2.GAMEID
                                    WHERE 
                                        Game.GAMEID = ?
                                        AND p1.PLAYERID = (SELECT MIN(PLAYERID) FROM Player WHERE GAMEID=Game.GAMEID)
                                        AND p2.PLAYERID = (SELECT MAX(PLAYERID) FROM Player WHERE GAMEID=Game.GAMEID)
                                """, (gameID+1,));
            result = cursor.fetchone();
            g, p1, p2 = result;
            
            self.gameID = gameID;
            self.gameName = g;
            self.player1Name = p1;
            self.player2Name = p2;

            cursor.close();
        
        #creating game based on values supplied by the calling function
        elif gameID is None and gameName is not None and isinstance(gameName, str) and player1Name is not None and isinstance(player1Name, str) and player2Name is not None and isinstance(player2Name, str):
            cursor = Database.conn.cursor();

            self.gameName = gameName;
            self.player1Name = player1Name;
            self.player2Name = player2Name;

            #update database with values for the new game
            cursor.execute("""INSERT
                                    INTO Game(GAMENAME)
                                    VALUES (?)""",
                                    (self.gameName,));
            self.gameID = cursor.lastrowid;
            cursor.execute("""INSERT
                                    INTO Player(GAMEID, PLAYERNAME)
                                    VALUES (?, ?)""",
                                    (self.gameID, self.player1Name));
            cursor.execute("""INSERT
                                    INTO Player(GAMEID, PLAYERNAME)
                                    VALUES (?, ?)""",
                                    (self.gameID, self.player2Name));

            cursor.close();
            Database.conn.commit();
        
        #raise TypeError if invalid arguments are passed to the function
        else:
            raise TypeError("Invalid arguments passed to Game constructor.");

    def shoot( self, gameName, playerName, table, xvel, yvel ):
        """
        This function simulates a shot in a game of pool.
        """
        
        cursor = Database.conn.cursor();

        #retrieve playerID and gameID to update Shot table
        cursor.execute("""SELECT GAMEID
                            FROM Game
                            WHERE Game.GAMENAME=?""", (gameName,));
        gameID = cursor.fetchone();
        cursor.execute("""SELECT PLAYERID
                            FROM Player
                            WHERE Player.PLAYERNAME=?
                                    AND Player.GAMEID=?""", (playerName, gameID[0]));
        playerID = cursor.fetchone();

        #update Shot table based on retrieved playerID and gameID values
        cursor.execute("""INSERT
                            INTO Shot(PLAYERID, GAMEID)
                            VALUES (?, ?)""",
                            (playerID[0], gameID[0]));
        shotID = cursor.lastrowid;

        xpos = None;
        ypos = None;
        
        #changing cue ball from a still ball to a rolling ball to begin the "shot"
        for object in table:
            if object is not None and isinstance(object, StillBall) and object.obj.still_ball.number==0:
                xpos = object.obj.still_ball.pos.x;
                ypos = object.obj.still_ball.pos.y;

                object.type = phylib.PHYLIB_ROLLING_BALL;

                object.obj.rolling_ball.pos.x = xpos;
                object.obj.rolling_ball.pos.y = ypos;

                object.obj.rolling_ball.vel.x = xvel;
                object.obj.rolling_ball.vel.y = yvel;

                speed = math.sqrt(xvel**2 + yvel**2);
                xacc = 0;
                yacc = 0;
                if (speed > VEL_EPSILON):
                    xacc = (-1)*(xvel)/speed*DRAG;
                    yacc = (-1)*(yvel)/speed*DRAG;
                object.obj.rolling_ball.acc.x = xacc;
                object.obj.rolling_ball.acc.y = yacc;

                object.obj.rolling_ball.number = 0;
                

        svgFrames = []; #an array of SVGs, where each SVG represents a single "frame" of the shot

        #write the "shot" to the database frame-by-frame
        while table:
            
            startTime = table.time;
            startingTable = table;

            table = table.segment(); #entirety of the "shot"

            if table is not None:
                
                endTime = table.time;
                length = endTime - startTime; #duration of shot in seconds
                length /= FRAME_INTERVAL;
                length = math.floor(length); #number of frames for the shot

                for i in range(0, length+1): #write each individual frame of the shot to the database
                    
                    curr = i*FRAME_INTERVAL;
                    currentTable = startingTable.roll(curr);
                    currentTable.time = startTime + curr;

                    tableID = self.db.writeTable(currentTable);
                    cursor.execute("""INSERT
                                        INTO TableShot(TABLEID, SHOTID)
                                        VALUES (?, ?)""",
                                        (tableID+1, shotID));

                    currentSvg = currentTable.svg();
                    svgFrames.append(currentSvg);
                
        
        
        cursor.close();
        Database.conn.commit();
        
        return svgFrames;