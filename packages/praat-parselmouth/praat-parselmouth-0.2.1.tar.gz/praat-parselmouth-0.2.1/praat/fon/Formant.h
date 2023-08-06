#ifndef _Formant_h_
#define _Formant_h_
/* Formant.h
 *
 * Copyright (C) 1992-2011,2015 Paul Boersma
 *
 * This code is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or (at
 * your option) any later version.
 *
 * This code is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this work. If not, see <http://www.gnu.org/licenses/>.
 */

#include "Matrix.h"
#include "Table.h"
Thing_declare (Interpreter);

#include "Formant_def.h"

autoFormant Formant_create (double tmin, double tmax, long nt, double dt, double t1, int maxnFormants);
/*
	Function:
		return a new instance of Formant.
	Preconditions:
		nt >= 1;
		dt > 0.0;
		maxnFormants >= 1;
	Postconditions:
		my xmin = tmin;
		my xmax = tmax;
		my nx = nt;
		my dx = dt;
		my x1 = t1;
		my maximumNumberOfPairs == maxnFormants;
		my frames [1..nt]. intensity == 0.0;
		my frames [1..nt]. numberOfPairs == 0;
		my frames [1..nt]. formants [1..maxnFormants] = 0.0;
		my frames [1..nt]. bandwidths [1..maxnFormants] = 0.0;
*/
long Formant_getMinNumFormants (Formant me);
long Formant_getMaxNumFormants (Formant me);

double Formant_getValueAtTime (Formant me, int iformant, double time, int bark);
double Formant_getBandwidthAtTime (Formant me, int iformant, double time, int bark);

void Formant_getExtrema (Formant me, int iformant, double tmin, double tmax, double *fmin, double *fmax);
void Formant_getMinimumAndTime (Formant me, int iformant, double tmin, double tmax, int bark, int interpolate,
	double *return_minimum, double *return_timeOfMinimum);
void Formant_getMaximumAndTime (Formant me, int iformant, double tmin, double tmax, int bark, int interpolate,
	double *return_maximum, double *return_timeOfMaximum);
double Formant_getMinimum (Formant me, int iformant, double tmin, double tmax, int bark, int interpolate);
double Formant_getMaximum (Formant me, int iformant, double tmin, double tmax, int bark, int interpolate);
double Formant_getTimeOfMaximum (Formant me, int iformant, double tmin, double tmax, int bark, int interpolate);
double Formant_getTimeOfMinimum (Formant me, int iformant, double tmin, double tmax, int bark, int interpolate);

double Formant_getQuantile (Formant me, int iformant, double quantile, double tmin, double tmax, int bark);
double Formant_getQuantileOfBandwidth (Formant me, int iformant, double quantile, double tmin, double tmax, int bark);
double Formant_getMean (Formant me, int iformant, double tmin, double tmax, int bark);
double Formant_getStandardDeviation (Formant me, int iformant, double tmin, double tmax, int bark);

void Formant_sort (Formant me);

void Formant_drawTracks (Formant me, Graphics g, double tmin, double tmax, double fmax, int garnish);
void Formant_drawSpeckles_inside (Formant me, Graphics g, double tmin, double tmax, double fmin, double fmax,
	double suppress_dB);
void Formant_drawSpeckles (Formant me, Graphics g, double tmin, double tmax, double fmax,
	double suppress_dB, int garnish);
void Formant_scatterPlot (Formant me, Graphics g, double tmin, double tmax,
	int iformant1, double fmin1, double fmax1, int iformant2, double fmin2, double fmax2,
	double size_mm, const char32 *mark, int garnish);

autoMatrix Formant_to_Matrix (Formant me, int iformant);
autoMatrix Formant_to_Matrix_bandwidths (Formant me, int iformant);
void Formant_formula_frequencies (Formant me, const char32 *formula, Interpreter interpreter);
void Formant_formula_bandwidths (Formant me, const char32 *formula, Interpreter interpreter);

autoFormant Formant_tracker (Formant me, int numberOfTracks,
	double refF1, double refF2, double refF3, double refF4, double refF5,
	double dfCost,   // per kHz
	double bfCost, double octaveJumpCost);

autoTable Formant_downto_Table (Formant me, bool includeFrameNumbers,
	bool includeTimes, int timeDecimals,
	bool includeIntensity, int intensityDecimals,
	bool includeNumberOfFormants, int frequencyDecimals,
	bool includeBandwidths);
void Formant_list (Formant me, bool includeFrameNumbers,
	bool includeTimes, int timeDecimals,
	bool includeIntensity, int intensityDecimals,
	bool includeNumberOfFormants, int frequencyDecimals,
	bool includeBandwidths);

/* End of file Formant.h */
#endif
