#include "phylib.h"

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>



/*creates still-ball object
number holds number of pool ball; pos holds position vector
returns the still-ball object*/
phylib_object *phylib_new_still_ball( unsigned char number,
                                        phylib_coord *pos ) {
	phylib_object* ball = (phylib_object*) calloc(1, sizeof(phylib_object)); //new still ball
	if (ball != NULL) {
		ball->type = PHYLIB_STILL_BALL;
		ball->obj.still_ball.number = number;
		ball->obj.still_ball.pos = *pos;
	}
	return ball;
}

/*creates rolling-ball object
number holds number of pool ball; pos, vel, and acc hold position, velocity, and acceleration vectors
returns the rolling-ball object*/
phylib_object *phylib_new_rolling_ball( unsigned char number,
                                        phylib_coord *pos,
                                        phylib_coord *vel,
                                        phylib_coord *acc ) {
	phylib_object* ball = (phylib_object*) malloc(sizeof(phylib_object)); //new rolling ball
	if (ball != NULL) {
		ball->type = PHYLIB_ROLLING_BALL;
		ball->obj.rolling_ball.number = number;
		ball->obj.rolling_ball.pos = *pos;
		ball->obj.rolling_ball.vel = *vel;
		ball->obj.rolling_ball.acc = *acc;
	}
	return ball;
}

/*creates hole object
pos holds position vector
returns the hole object*/
phylib_object *phylib_new_hole( phylib_coord *pos ) {
	phylib_object* hole = (phylib_object*) malloc(sizeof(phylib_object)); //new hole
	if (hole != NULL) {
		hole->type = PHYLIB_HOLE;
		hole->obj.hole.pos = *pos;
	}
	return hole;
}

/*creates horizontal-cushion object
y holds y-coordinate of cushion
returns the cushion object*/
phylib_object *phylib_new_hcushion( double y ) {
	phylib_object* cushion = (phylib_object*) malloc(sizeof(phylib_object)); //new horizontal cushion
	if (cushion != NULL) {
		cushion->type = PHYLIB_HCUSHION;
		cushion->obj.hcushion.y = y;
	}
	return cushion;
}

/*creates vertical-cushion object
x holds x-coordinate of cushion
returns the cushion object*/
phylib_object *phylib_new_vcushion( double x ) {
        phylib_object* cushion = (phylib_object*) malloc(sizeof(phylib_object)); //new vertical cushion
        if (cushion != NULL) {
                cushion->type = PHYLIB_VCUSHION;
                cushion->obj.vcushion.x = x;
        }
        return cushion;
}

/*creates table and initializes various objects
returns the table*/
phylib_table *phylib_new_table( void ) {
	phylib_table* table = (phylib_table*) malloc(sizeof(phylib_table)); //new table
	if (table != NULL) {
		table->time = 0.0;
		table->object[0] = phylib_new_hcushion(0.0); //top cushion
		table->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH); //bottom cushion
		table->object[2] = phylib_new_vcushion(0.0); //left cushion
		table->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH); //right cushion

		phylib_coord topLeft;
		topLeft.x = 0;
		topLeft.y = 0;
		phylib_coord middleLeft;
		middleLeft.x = 0;
		middleLeft.y = PHYLIB_TABLE_WIDTH;
		phylib_coord bottomLeft;
		bottomLeft.x = 0;
		bottomLeft.y = PHYLIB_TABLE_LENGTH;
		phylib_coord topRight;
		topRight.x = PHYLIB_TABLE_WIDTH;
		topRight.y = 0;
		phylib_coord middleRight;
		middleRight.x = PHYLIB_TABLE_WIDTH;
		middleRight.y = PHYLIB_TABLE_WIDTH;
		phylib_coord bottomRight;
		bottomRight.x = PHYLIB_TABLE_WIDTH;
		bottomRight.y = PHYLIB_TABLE_LENGTH;

		table->object[4] = phylib_new_hole(&topLeft);
                table->object[5] = phylib_new_hole(&middleLeft);
                table->object[6] = phylib_new_hole(&bottomLeft);
                table->object[7] = phylib_new_hole(&topRight);
                table->object[8] = phylib_new_hole(&middleRight);
                table->object[9] = phylib_new_hole(&bottomRight);
		for (int i=10; i<PHYLIB_MAX_OBJECTS; i++) { //initialize remaining objects on table to NULL
			table->object[i] = NULL;
		}
	}
	return table;
}

/*creates a copy of an object
src is the object being copied, dest is the new copy*/
void phylib_copy_object( phylib_object **dest, phylib_object **src ) {
	if (*src == NULL) { //handling case where object to be copied is NULL
		*dest = NULL;
	}
	else { //otherwise allocate memory and copy object
		*dest = (phylib_object*) malloc(sizeof(phylib_object));
		memcpy(*dest, *src, sizeof(phylib_object));
	}
}

/*creates a copy of the table and all object on it
table is the object being copied
returns the copy of the table*/
phylib_table *phylib_copy_table( phylib_table *table ) {
	phylib_table* dest = (phylib_table*) malloc(sizeof(phylib_table)); //allocate memory for copy of table
	if (dest != NULL) { //if table to be copied is not NULL, copy table and objects on it
		memcpy(dest, table, sizeof(phylib_table));
		for (int i=0; i<PHYLIB_MAX_OBJECTS; i++) {
			phylib_copy_object( &dest->object[i], &table->object[i] );
		}
	}
	return dest;
}

/*adds an object to the table
object holds the object to be added, table holds the table to add to*/
void phylib_add_object( phylib_table *table, phylib_object *object ) {
	int done = 0; //exit function once object has been added
	for (int i=0; i<PHYLIB_MAX_OBJECTS && done==0; i++) { //search for first NULL slot on table
		if (table->object[i] == NULL) {
			table->object[i] = object;
			done = 1;
		}
	}
}

/*frees the table and all objects on it
table holds the table to be freed*/
void phylib_free_table( phylib_table *table ) {
	for (int i=0; i<PHYLIB_MAX_OBJECTS; i++) { //free all objects on table
		if (table->object[i] != NULL) {
			free(table->object[i]);
			table->object[i] = NULL;
		}
	}
	if (table != NULL) { //free the table
		free(table);
	}
}

/*subtracts two vectors
c2 is subtracted from c1
returns the difference vector*/
phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 ) {
	phylib_coord c; //difference vector
	c.x = c1.x - c2.x;
	c.y = c1.y - c2.y;
	return c;
}

/*calculates length of a vector
c is the vector in question
returns the length*/
double phylib_length( phylib_coord c ) {
	double len = sqrt((c.x * c.x) + (c.y * c.y)); //length of c
	return len;
}

/*performs dot product on two vectors
a and b are the two vectors
returns the dot product*/
double phylib_dot_product( phylib_coord a, phylib_coord b ) {
	double dp = ((a.x * b.x) + (a.y * b.y)); //dot product of a and b
	return dp;
}

/*calculates distance between rolling-ball and another object
obj1 is the rolling-ball, obj2 is the other object
returns the distance*/
double phylib_distance( phylib_object *obj1, phylib_object *obj2 ) {
	double distance = -1.0; //distance between two objects, -1.0 if types are invalid

	if (obj1->type == PHYLIB_ROLLING_BALL) {
		switch (obj2->type) {
			case PHYLIB_STILL_BALL:
				distance = phylib_length( phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.still_ball.pos) );
				distance -= PHYLIB_BALL_DIAMETER;
				break;
			case PHYLIB_ROLLING_BALL:
				distance = phylib_length( phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.rolling_ball.pos) );
				distance -= PHYLIB_BALL_DIAMETER;
				break;
			case PHYLIB_HOLE:
				distance = phylib_length( phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.hole.pos) );
				distance -= PHYLIB_HOLE_RADIUS;
				break;
			case PHYLIB_HCUSHION:
				distance = fabs(obj1->obj.rolling_ball.pos.y - obj2->obj.hcushion.y);
				distance -= PHYLIB_BALL_RADIUS;
				break;
			case PHYLIB_VCUSHION:
				distance = fabs(obj1->obj.rolling_ball.pos.x - obj2->obj.vcushion.x);
				distance -= PHYLIB_BALL_RADIUS;
				break;
		}
	}

	return distance;
}

/*updates a rolling-ball after it has rolled for a period of time
new is the updated rolling-ball, old is the original rolling-ball, time is the duration of the roll*/
void phylib_roll( phylib_object *new, phylib_object *old, double time ) {
	if (new->type==PHYLIB_ROLLING_BALL && old->type==PHYLIB_ROLLING_BALL) { //exit function if object isn't a rolling ball
		//update positions
		new->obj.rolling_ball.pos.x = old->obj.rolling_ball.pos.x + (old->obj.rolling_ball.vel.x)*(time) + (0.5)*(old->obj.rolling_ball.acc.x)*(time*time);
		new->obj.rolling_ball.pos.y = old->obj.rolling_ball.pos.y + (old->obj.rolling_ball.vel.y)*(time) + (0.5)*(old->obj.rolling_ball.acc.y)*(time*time);

		//update velocities
		new->obj.rolling_ball.vel.x = old->obj.rolling_ball.vel.x + (old->obj.rolling_ball.acc.x)*(time);
		new->obj.rolling_ball.vel.y = old->obj.rolling_ball.vel.y + (old->obj.rolling_ball.acc.y)*(time);

		//if ball changed direction for x or y component, set that component's vel and acc to zero
		if ( (new->obj.rolling_ball.vel.x) * (old->obj.rolling_ball.vel.x) < 0 ) {
			new->obj.rolling_ball.vel.x = 0;
			new->obj.rolling_ball.acc.x = 0;
		}
		if ( (new->obj.rolling_ball.vel.y) * (old->obj.rolling_ball.vel.y) < 0 ) {
			new->obj.rolling_ball.vel.y = 0;
			new->obj.rolling_ball.acc.y = 0;
		}
	}
}

/*determines if a rolling-ball has stopped rolling and converts it to a still-ball if it has
object is the rolling-ball in question
returns 1 if it has stopped, 0 otherwise*/
unsigned char phylib_stopped( phylib_object *object ) {
	if (phylib_length(object->obj.rolling_ball.vel) < PHYLIB_VEL_EPSILON) { //if speed is under a certain threshold
		//copy over data stored within object after changing its type
		unsigned char number = object->obj.rolling_ball.number;
		double x = object->obj.rolling_ball.pos.x;
		double y = object->obj.rolling_ball.pos.y;
		object->type = PHYLIB_STILL_BALL;
		object->obj.still_ball.number = number;
		object->obj.still_ball.pos.x = x;
		object->obj.still_ball.pos.y = y;
		return 1;
	}
	return 0;
}

/*simulates a rolling-ball hitting another object
a is the rolling-ball, b is the object being hit*/
void phylib_bounce( phylib_object **a, phylib_object **b ) {
	switch ((*b)->type) {
		case PHYLIB_HCUSHION: //horizontal reflection
			(*a)->obj.rolling_ball.vel.y *= -1;
			(*a)->obj.rolling_ball.acc.y *= -1;
			break;
		case PHYLIB_VCUSHION: //vertical reflection
			(*a)->obj.rolling_ball.vel.x *= -1;
                        (*a)->obj.rolling_ball.acc.x *= -1;
			break;
		case PHYLIB_HOLE: //remove ball from table
			if ( *a!=NULL ) {
				free(*a);
				*a = NULL;
			}
			break;
		case PHYLIB_STILL_BALL: //convert to rolling ball and proceed to next case
			(*b)->type = PHYLIB_ROLLING_BALL;
		case PHYLIB_ROLLING_BALL: //computes various physics
			; //somehow fixes scope issues with creating variables in a switch case

			//position of a relative to b
			phylib_coord r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);

			//velocity of a relative to b
			phylib_coord v_rel = phylib_sub( (*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel );

			double len_r_ab = phylib_length(r_ab); //length of r_ab
			phylib_coord n; //normal vector
			if (len_r_ab != 0) {
				n.x = r_ab.x / len_r_ab;
				n.y = r_ab.y / len_r_ab;
			}
			else {
				n.x = 0;
				n.y = 0;
			}

			double v_rel_n = phylib_dot_product(v_rel, n); //dot product of v_rel relative to n

			//update velocities of both balls
			(*a)->obj.rolling_ball.vel.x -= (v_rel_n)*(n.x);
			(*a)->obj.rolling_ball.vel.y -= (v_rel_n)*(n.y);
			(*b)->obj.rolling_ball.vel.x += (v_rel_n)*(n.x);
			(*b)->obj.rolling_ball.vel.y += (v_rel_n)*(n.y);

			double speed_a = phylib_length((*a)->obj.rolling_ball.vel); //speed of a
			if (speed_a > PHYLIB_VEL_EPSILON) { //introducing drag when ball is rolling
				(*a)->obj.rolling_ball.acc.x = ((*a)->obj.rolling_ball.vel.x)*(-1) / speed_a * PHYLIB_DRAG;
				(*a)->obj.rolling_ball.acc.y = ((*a)->obj.rolling_ball.vel.y)*(-1) / speed_a * PHYLIB_DRAG;
			}
			double speed_b = phylib_length((*b)->obj.rolling_ball.vel); //speed of b
			if (speed_b > PHYLIB_VEL_EPSILON) {
				(*b)->obj.rolling_ball.acc.x = ((*b)->obj.rolling_ball.vel.x)*(-1) / speed_b * PHYLIB_DRAG;
				(*b)->obj.rolling_ball.acc.y = ((*b)->obj.rolling_ball.vel.y)*(-1) / speed_b * PHYLIB_DRAG;
			}
			break;
	}
}

/*determines number of rolling-balls on table
t is the table
returns number of rolling-balls*/
unsigned char phylib_rolling( phylib_table *t ) {
	unsigned char num = 0; //number of rolling balls on table
	for (int i=0; i<PHYLIB_MAX_OBJECTS; i++) {
		if (t->object[i]!=NULL && t->object[i]->type == PHYLIB_ROLLING_BALL) {
			num++;
		}
	}
	return num;
}

/*simulates the entire pool table for a "segment" of time
table holds the pool table
returns the updated pool table after the "segment"*/
phylib_table *phylib_segment( phylib_table *table ) {
    if (phylib_rolling(table) == 0) { //nothing to be done if no balls are rolling
        return NULL;
    }

	phylib_table* updated = phylib_copy_table(table); //updated table to be returned (i.e. table after the "segment")

	double max = PHYLIB_MAX_TIME / PHYLIB_SIM_RATE;
    for (double current=1; current<=max; current++) { //loop until max time is reached
        for (int i=0; i<PHYLIB_MAX_OBJECTS; i++) { //roll balls
            if (table->object[i]!=NULL && table->object[i]->type==PHYLIB_ROLLING_BALL) {
                phylib_roll(updated->object[i], table->object[i], current*PHYLIB_SIM_RATE);
			}
		}

        updated->time = table->time + current*PHYLIB_SIM_RATE; //update time

		for (int i=0; i<PHYLIB_MAX_OBJECTS; i++) { //after rolling all balls, check for stops and collisions
			if (table->object[i]!=NULL && table->object[i]->type==PHYLIB_ROLLING_BALL) { //checking for stopped balls
            	if (phylib_stopped(updated->object[i])) {
                	return updated;
            	}

            	for (int j=0; j<PHYLIB_MAX_OBJECTS; j++) { //checking for collisions
                	if (j!=i && updated->object[j]!=NULL && phylib_distance(updated->object[i], updated->object[j]) < 0.0) {
                    	phylib_bounce(&updated->object[i], &updated->object[j]);
                    	return updated;
                	}
            	}
			}
        }
    }

    return updated;
}

char *phylib_object_string( phylib_object *object )
{
	static char string[80];
	if (object==NULL)
	{
		snprintf( string, 80, "NULL;" );
		return string;
	}

	switch (object->type)
	{
		case PHYLIB_STILL_BALL:
			snprintf( string, 80,
				"STILL_BALL (%d,%6.1lf,%6.1lf)",
				object->obj.still_ball.number,
				object->obj.still_ball.pos.x,
				object->obj.still_ball.pos.y );
			break;
		case PHYLIB_ROLLING_BALL:
			snprintf( string, 80,
				"ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
				object->obj.rolling_ball.number,
				object->obj.rolling_ball.pos.x,
				object->obj.rolling_ball.pos.y,
				object->obj.rolling_ball.vel.x,
				object->obj.rolling_ball.vel.y,
				object->obj.rolling_ball.acc.x,
				object->obj.rolling_ball.acc.y );
			break;
		case PHYLIB_HOLE:
			snprintf( string, 80,
				"HOLE (%6.1lf,%6.1lf)",
				object->obj.hole.pos.x,
				object->obj.hole.pos.y );
			break;
		case PHYLIB_HCUSHION:
			snprintf( string, 80,
				"HCUSHION (%6.1lf)",
				object->obj.hcushion.y );
			break;
		case PHYLIB_VCUSHION:
			snprintf( string, 80,
				"VCUSHION (%6.1lf)",
				object->obj.vcushion.x );
			break;
	}
	return string;
}
