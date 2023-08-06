/* OTGrammarEditor.cpp
 *
 * Copyright (C) 1997-2011,2012,2013,2015,2016 Paul Boersma
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

/*
 * a selection of changes:
 * pb 2003/05/27 learnOne and learnOneFromPartialOutput
 * pb 2008/05/31 ExponentialMaximumEntropy
 */

#include "OTGrammarEditor.h"
#include "EditorM.h"

Thing_implement (OTGrammarEditor, HyperPage, 0);

static void menu_cb_evaluate (OTGrammarEditor me, EDITOR_ARGS_FORM) {
	EDITOR_FORM (U"Evaluate", nullptr)
		REAL (U"Noise", U"2.0")
	EDITOR_OK
	EDITOR_DO
		Editor_save (me, U"Evaluate");
		OTGrammar_newDisharmonies ((OTGrammar) my data, GET_REAL (U"Noise"));
		Graphics_updateWs (my graphics.get());
		Editor_broadcastDataChanged (me);
	EDITOR_END
}

static void menu_cb_evaluate_noise_2_0 (OTGrammarEditor me, EDITOR_ARGS_DIRECT) {
	Editor_save (me, U"Evaluate (noise 2.0)");
	OTGrammar_newDisharmonies ((OTGrammar) my data, 2.0);
	Graphics_updateWs (my graphics.get());
	Editor_broadcastDataChanged (me);
}

static void menu_cb_evaluate_tinyNoise (OTGrammarEditor me, EDITOR_ARGS_DIRECT) {
	Editor_save (me, U"Evaluate (tiny noise)");
	OTGrammar_newDisharmonies ((OTGrammar) my data, 1e-9);
	Graphics_updateWs (my graphics.get());
	Editor_broadcastDataChanged (me);
}

static void menu_cb_evaluate_zeroNoise (OTGrammarEditor me, EDITOR_ARGS_DIRECT) {
	Editor_save (me, U"Evaluate (zero noise)");
	OTGrammar_newDisharmonies ((OTGrammar) my data, 0.0);
	Graphics_updateWs (my graphics.get());
	Editor_broadcastDataChanged (me);
}

static void menu_cb_editConstraint (OTGrammarEditor me, EDITOR_ARGS_FORM) {
	EDITOR_FORM (U"Edit constraint", nullptr)
		LABEL (U"constraint", U"");
		REAL (U"Ranking value", U"100.0");
		REAL (U"Disharmony", U"100.0");
		REAL (U"Plasticity", U"1.0");
	EDITOR_OK
		OTGrammar ot = (OTGrammar) my data;
		OTGrammarConstraint constraint;
		if (my selected < 1 || my selected > ot -> numberOfConstraints)
			Melder_throw (U"Select a constraint first.");
		constraint = & ot -> constraints [ot -> index [my selected]];
		SET_STRING (U"constraint", constraint -> name)
		SET_REAL (U"Ranking value", constraint -> ranking)
		SET_REAL (U"Disharmony", constraint -> disharmony)
		SET_REAL (U"Plasticity", constraint -> plasticity)
	EDITOR_DO
		OTGrammar ot = (OTGrammar) my data;
		OTGrammarConstraint constraint = & ot -> constraints [ot -> index [my selected]];
		Editor_save (me, U"Edit constraint");
		constraint -> ranking = GET_REAL (U"Ranking value");
		constraint -> disharmony = GET_REAL (U"Disharmony");
		constraint -> plasticity = GET_REAL (U"Plasticity");
		OTGrammar_sort (ot);
		Graphics_updateWs (my graphics.get());
		Editor_broadcastDataChanged (me);
	EDITOR_END
}

static void menu_cb_learnOne (OTGrammarEditor me, EDITOR_ARGS_FORM) {
	EDITOR_FORM (U"Learn one", U"OTGrammar: Learn one...")
		LABEL (U"", U"Underlying form:")
		SENTENCE (U"Input string", U"")
		LABEL (U"", U"Adult surface form:")
		SENTENCE (U"Output string", U"")
		REAL (U"Evaluation noise", U"2.0")
		OPTIONMENU_ENUM (U"Update rule", kOTGrammar_rerankingStrategy, kOTGrammar_rerankingStrategy_SYMMETRIC_ALL)
		REAL (U"Plasticity", U"0.1")
		REAL (U"Rel. plasticity spreading", U"0.1")
		BOOLEAN (U"Honour local rankings", 1)
	EDITOR_OK
	EDITOR_DO
		Editor_save (me, U"Learn one");
		OTGrammar_learnOne ((OTGrammar) my data, GET_STRING (U"Input string"), GET_STRING (U"Output string"),
			GET_REAL (U"Evaluation noise"), GET_ENUM (kOTGrammar_rerankingStrategy, U"Update rule"), GET_INTEGER (U"Honour local rankings"),
			GET_REAL (U"Plasticity"), GET_REAL (U"Rel. plasticity spreading"), true, true, nullptr);
		OTGrammar_sort ((OTGrammar) my data);
		Graphics_updateWs (my graphics.get());
		Editor_broadcastDataChanged (me);
	EDITOR_END
}

static void menu_cb_learnOneFromPartialOutput (OTGrammarEditor me, EDITOR_ARGS_FORM) {
	EDITOR_FORM (U"Learn one from partial adult output", 0)
		LABEL (U"", U"Partial adult surface form (e.g. overt form):")
		SENTENCE (U"Partial output", U"")
		REAL (U"Evaluation noise", U"2.0")
		OPTIONMENU_ENUM (U"Update rule", kOTGrammar_rerankingStrategy, kOTGrammar_rerankingStrategy_SYMMETRIC_ALL)
		REAL (U"Plasticity", U"0.1")
		REAL (U"Rel. plasticity spreading", U"0.1")
		BOOLEAN (U"Honour local rankings", 1)
		NATURAL (U"Number of chews", U"1")
	EDITOR_OK
	EDITOR_DO
		Editor_save (me, U"Learn one from partial output");
		OTGrammar_learnOneFromPartialOutput ((OTGrammar) my data, GET_STRING (U"Partial output"),
			GET_REAL (U"Evaluation noise"), GET_ENUM (kOTGrammar_rerankingStrategy, U"Update rule"), GET_INTEGER (U"Honour local rankings"),
			GET_REAL (U"Plasticity"), GET_REAL (U"Rel. plasticity spreading"), GET_INTEGER (U"Number of chews"), true);
		OTGrammar_sort ((OTGrammar) my data);
		Graphics_updateWs (my graphics.get());
		Editor_broadcastDataChanged (me);
	EDITOR_END
}

static void menu_cb_removeConstraint (OTGrammarEditor me, EDITOR_ARGS_DIRECT) {
	OTGrammar ot = (OTGrammar) my data;
	OTGrammarConstraint constraint;
	if (my selected < 1 || my selected > ot -> numberOfConstraints)
		Melder_throw (U"Select a constraint first.");
	constraint = & ot -> constraints [ot -> index [my selected]];
	Editor_save (me, U"Remove constraint");
	OTGrammar_removeConstraint (ot, constraint -> name);
	Graphics_updateWs (my graphics.get());
	Editor_broadcastDataChanged (me);
}

static void menu_cb_resetAllRankings (OTGrammarEditor me, EDITOR_ARGS_FORM) {
	EDITOR_FORM (U"Reset all rankings", 0)
		REAL (U"Ranking", U"100.0")
	EDITOR_OK
	EDITOR_DO
		Editor_save (me, U"Reset all rankings");
		OTGrammar_reset ((OTGrammar) my data, GET_REAL (U"Ranking"));
		Graphics_updateWs (my graphics.get());
		Editor_broadcastDataChanged (me);
	EDITOR_END
}

static void menu_cb_OTGrammarEditor_help (OTGrammarEditor, EDITOR_ARGS_DIRECT) { Melder_help (U"OTGrammarEditor"); }
static void menu_cb_OTGrammar_help (OTGrammarEditor, EDITOR_ARGS_DIRECT) { Melder_help (U"OTGrammar"); }
static void menu_cb_OTLearningTutorial (OTGrammarEditor, EDITOR_ARGS_DIRECT) { Melder_help (U"OT learning"); }

void structOTGrammarEditor :: v_createMenus () {
	OTGrammarEditor_Parent :: v_createMenus ();
	Editor_addCommand (this, U"Edit", U"-- edit ot --", 0, nullptr);
	Editor_addCommand (this, U"Edit", U"Evaluate...", 0, menu_cb_evaluate);
	Editor_addCommand (this, U"Edit", U"Evaluate (noise 2.0)", '2', menu_cb_evaluate_noise_2_0);
	Editor_addCommand (this, U"Edit", U"Evaluate (zero noise)", '0', menu_cb_evaluate_zeroNoise);
	Editor_addCommand (this, U"Edit", U"Evaluate (tiny noise)", '9', menu_cb_evaluate_tinyNoise);
	Editor_addCommand (this, U"Edit", U"Edit constraint...", 'E', menu_cb_editConstraint);
	Editor_addCommand (this, U"Edit", U"Reset all rankings...", 'R', menu_cb_resetAllRankings);
	Editor_addCommand (this, U"Edit", U"Learn one...", 0, menu_cb_learnOne);
	Editor_addCommand (this, U"Edit", U"Learn one from partial output...", '1', menu_cb_learnOneFromPartialOutput);
	Editor_addCommand (this, U"Edit", U"-- remove ot --", 0, nullptr);
	Editor_addCommand (this, U"Edit", U"Remove constraint", 0, menu_cb_removeConstraint);
}

void structOTGrammarEditor :: v_createHelpMenuItems (EditorMenu menu) {
	OTGrammarEditor_Parent :: v_createHelpMenuItems (menu);
	EditorMenu_addCommand (menu, U"OTGrammarEditor help", '?', menu_cb_OTGrammarEditor_help);
	EditorMenu_addCommand (menu, U"OTGrammar help", 0, menu_cb_OTGrammar_help);
	EditorMenu_addCommand (menu, U"OT learning tutorial", 0, menu_cb_OTLearningTutorial);
}

static OTGrammar drawTableau_ot;
static const char32 *drawTableau_input;
static bool drawTableau_constraintsAreDrawnVertically;
static void drawTableau (Graphics g) {
	OTGrammar_drawTableau (drawTableau_ot, g, drawTableau_constraintsAreDrawnVertically, drawTableau_input);
}

void structOTGrammarEditor :: v_draw () {
	OTGrammar ot = (OTGrammar) data;
	static char32 text [1000];
	Graphics_clearWs (graphics.get());
	if (ot -> decisionStrategy == kOTGrammar_decisionStrategy_EXPONENTIAL_HG ||
		ot -> decisionStrategy == kOTGrammar_decisionStrategy_EXPONENTIAL_MAXIMUM_ENTROPY)
	{
		HyperPage_listItem (this, U"\t\t      %%ranking value\t      %disharmony\t      %plasticity\t   %%e^^disharmony");
	} else {
		HyperPage_listItem (this, U"\t\t      %%ranking value\t      %disharmony\t      %plasticity");
	}
	for (long icons = 1; icons <= ot -> numberOfConstraints; icons ++) {
		OTGrammarConstraint constraint = & ot -> constraints [ot -> index [icons]];
		if (ot -> decisionStrategy == kOTGrammar_decisionStrategy_EXPONENTIAL_HG ||
			ot -> decisionStrategy == kOTGrammar_decisionStrategy_EXPONENTIAL_MAXIMUM_ENTROPY)
		{
			Melder_sprint (text,1000,
				U"\t", icons == selected ? U"♠︎ " : U"   ",
				U"@@", icons,
				U"|", constraint -> name,
				U"@\t      ", Melder_fixed (constraint -> ranking, 3),
				U"\t      ", Melder_fixed (constraint -> disharmony, 3),
				U"\t      ", Melder_fixed (constraint -> plasticity, 6),
				U"\t ", Melder_float (Melder_half (exp (constraint -> disharmony))));
		} else {
			Melder_sprint (text,1000,
				U"\t", icons == selected ? U"♠︎ " : U"   ",
				U"@@", icons,
				U"|", constraint -> name,
				U"@\t      ", Melder_fixed (constraint -> ranking, 3),
				U"\t      ", Melder_fixed (constraint -> disharmony, 3),
				U"\t      ", Melder_fixed (constraint -> plasticity, 6));
		}
		HyperPage_listItem (this, text);
	}
	Graphics_setAtSignIsLink (graphics.get(), false);
	for (long itab = 1; itab <= ot -> numberOfTableaus; itab ++) {
		OTGrammarTableau tableau = & ot -> tableaus [itab];
		double rowHeight = 0.25;
		double tableauHeight = rowHeight * (tableau -> numberOfCandidates + 2);
		drawTableau_ot = ot;
		drawTableau_input = tableau -> input;
		drawTableau_constraintsAreDrawnVertically = d_constraintsAreDrawnVertically;
		HyperPage_picture (this, 20, tableauHeight, drawTableau);
	}
	Graphics_setAtSignIsLink (graphics.get(), true);
}

int structOTGrammarEditor :: v_goToPage (const char32 *title) {
	if (! title) return 1;
	selected = Melder_atoi (title);
	return 1;
}

autoOTGrammarEditor OTGrammarEditor_create (const char32 *title, OTGrammar ot) {
	try {
		autoOTGrammarEditor me = Thing_new (OTGrammarEditor);
		my data = ot;
		HyperPage_init (me.get(), title, ot);
		return me;
	} catch (MelderError) {
		Melder_throw (U"OTGrammar window not created.");
	}
}

/* End of file OTGrammarEditor.cpp */
