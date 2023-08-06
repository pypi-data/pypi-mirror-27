#ifndef _espeakdata_FileInMemory_h_
#define _espeakdata_FileInMemory_h_

/* espeakdata_FileInMemory.h
 * Copyright (C) David Weenink 2012
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or (at
 * your option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
 */

#include "FileInMemory.h"
#include "Table.h"

extern autoFileInMemorySet espeakdata_phons;

extern autoFileInMemorySet espeakdata_dicts;

extern autoFileInMemorySet espeakdata_voices;

extern autoFileInMemorySet espeakdata_variants;

autoFileInMemorySet create_espeakdata_phons ();

autoFileInMemorySet create_espeakdata_dicts ();

autoFileInMemorySet create_espeakdata_voices ();

autoFileInMemorySet create_espeakdata_variants ();

extern autoStrings espeakdata_voices_names;

extern autoStrings espeakdata_variants_names;

void espeakdata_praat_init ();

const char * espeakdata_get_voicedata (const char *data, long ndata, char *buf, long nbuf, long *index);

autoTable espeakdata_voices_to_Table (FileInMemorySet me);

autoStrings espeakdata_voices_getNames (Table me, long column);

// mask the char / char32
char * espeakdata_get_dict_data (const char *name, unsigned int *size);

const char * espeakdata_get_voice (const char *vname, long *numberOfBytes);

const char * espeakdata_get_voiceVariant (const char *vname, long *numberOfBytes);

#endif
