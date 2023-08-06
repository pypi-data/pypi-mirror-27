/* TableOfReal_and_SVD.cpp
 *
 * Copyright (C) 1993-2012, 2015 David Weenink
 *
 * This code is free software; you can redistribute it and/or modify
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
 djmw 20021009 GPL header
 djmw 20031107 Added TablesOfReal_to_GSVD.
 djmw 20051202 Extract left/right singular vectors.
*/

#include "TableOfReal_and_SVD.h"

#define MIN(m,n) ((m) < (n) ? (m) : (n))

autoTableOfReal SVD_to_TableOfReal (SVD me, long from, long to) {
	try {
		autoTableOfReal thee = TableOfReal_create (my numberOfRows, my numberOfColumns);
		SVD_synthesize (me, from, to, thy data);
		return thee;
	} catch (MelderError) {
		Melder_throw (me, U": no TableOfReal synthesized.");
	}
}

autoSVD TableOfReal_to_SVD (TableOfReal me) {
	try {
		autoSVD thee = SVD_create_d (my data, my numberOfRows, my numberOfColumns);
		return thee;
	} catch (MelderError) {
		Melder_throw (me, U": no SVD created.");
	}
}

autoTableOfReal SVD_extractLeftSingularVectors (SVD me) {
	try {
		long mn_min = MIN (my numberOfRows, my numberOfColumns);
		autoTableOfReal thee = TableOfReal_create (my numberOfRows, mn_min);
		NUMmatrix_copyElements (my u, thy data, 1, my numberOfRows, 1, mn_min);
		return thee;
	} catch (MelderError) {
		Melder_throw (me, U": left singular vector not extracted.");
	}
}

autoTableOfReal SVD_extractRightSingularVectors (SVD me) {
	try {
		long mn_min = MIN (my numberOfRows, my numberOfColumns);
		autoTableOfReal thee = TableOfReal_create (my numberOfColumns, mn_min);
		NUMmatrix_copyElements (my v, thy data, 1, my numberOfColumns, 1, mn_min);
		return thee;
	} catch (MelderError) {
		Melder_throw (me, U": right singular vector not extracted.");
	}
}

autoTableOfReal SVD_extractSingularValues (SVD me) {
	try {
		long mn_min = MIN (my numberOfRows, my numberOfColumns);
		autoTableOfReal thee = TableOfReal_create (1, mn_min);
		NUMvector_copyElements (my d, thy data[1], 1, mn_min);
		return thee;
	} catch (MelderError) {
		Melder_throw (me, U": singular values not extracted.");
	}
}

autoGSVD TablesOfReal_to_GSVD (TableOfReal me, TableOfReal thee) {
	try {
		if (my numberOfColumns != thy numberOfColumns) {
			Melder_throw (U"Both tables must have the same number of columns.");
		}
		autoGSVD him = GSVD_create_d (my data, my numberOfRows, my numberOfColumns, thy data, thy numberOfRows);
		return him;
	} catch (MelderError) {
		Melder_throw (U"GSVD not constructed from TablesOfReal.");
	}
}

/* End of file SVD_and_TableOfReal.cpp */
