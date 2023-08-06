#ifndef _ActivationList_h_
#define _ActivationList_h_
/* Activation.h
 * 
 * Copyright (C) 1993-2011, 2015-2016 David Weenink
 * 
 * This program is free oftware; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or (at
 * your option) any later version.
 * 
 * This code is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this work. If not, see <http://www.gnu.org/licenses/>.
 */

/*
 djmw 20020315 GPL header.
 djmw 20110505 Latest modification.
 */

#include "Matrix.h"

Thing_define (ActivationList, Matrix) {
};

/* Attributes:
   xmin				:1
   xmax				:#units
   nx				:#units
   dx				:1
   x1				:1
   ymin				:1
   ymax				:#patterns
   ny				:#patterns
   dy				:1
   y1				:1
   z[iy][ix]		:the activities
*/

void ActivationList_init (ActivationList me, long ny, long nx);

autoActivationList ActivationList_create (long ny, long nx);

autoActivationList Matrix_to_ActivationList (Matrix me);

autoMatrix ActivationList_to_Matrix (ActivationList me);

int _ActivationList_checkElements (ActivationList me);
/* Return 1 if all elements are in interval [0,1] else 0. */

#endif /* _ActivationList_h_ */
