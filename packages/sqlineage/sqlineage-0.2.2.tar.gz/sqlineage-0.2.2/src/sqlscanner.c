
#line 1 "src/sqlscanner.rl"
/*
 * A mini C-like language scanner.
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <Python.h>

#include "state_machine.h"

#define MIN(a,b) ((a) < (b) ? a : b)

static PyObject *SqlineageError;
static PyObject *callback = NULL;


#line 130 "src/sqlscanner.rl"



#line 25 "src/sqlscanner.c"
static const char _clang_actions[] = {
	0, 1, 0, 1, 1, 1, 2, 1, 
	3, 1, 4, 1, 5, 1, 8, 1, 
	9, 1, 10, 1, 11, 1, 12, 1, 
	14, 1, 15, 1, 16, 1, 17, 1, 
	18, 1, 19, 1, 20, 1, 21, 1, 
	22, 2, 0, 12, 2, 0, 13, 2, 
	5, 6, 2, 5, 7
};

static const char _clang_key_offsets[] = {
	0, 0, 2, 3, 4, 6, 12, 15, 
	16, 18, 21, 22, 43, 52, 53, 55, 
	59, 61, 64, 70, 73, 73
};

static const char _clang_trans_keys[] = {
	34, 92, 39, 10, 48, 57, 48, 57, 
	65, 70, 97, 102, 10, 92, 96, 10, 
	10, 42, 10, 42, 47, 10, 10, 34, 
	35, 39, 45, 46, 47, 48, 92, 94, 
	96, 33, 44, 49, 57, 58, 64, 65, 
	122, 123, 126, 46, 93, 95, 48, 57, 
	65, 91, 97, 122, 45, 42, 47, 46, 
	120, 48, 57, 48, 57, 46, 48, 57, 
	48, 57, 65, 70, 97, 102, 10, 92, 
	96, 0
};

static const char _clang_single_lengths[] = {
	0, 2, 1, 1, 0, 0, 3, 1, 
	2, 3, 1, 11, 3, 1, 2, 2, 
	0, 1, 0, 3, 0, 0
};

static const char _clang_range_lengths[] = {
	0, 0, 0, 0, 1, 3, 0, 0, 
	0, 0, 0, 5, 3, 0, 0, 1, 
	1, 1, 3, 0, 0, 0
};

static const char _clang_index_offsets[] = {
	0, 0, 3, 5, 7, 9, 13, 17, 
	19, 22, 26, 28, 45, 52, 54, 57, 
	61, 63, 66, 70, 74, 75
};

static const char _clang_trans_targs[] = {
	11, 0, 1, 11, 2, 11, 3, 16, 
	11, 18, 18, 18, 11, 6, 7, 11, 
	6, 6, 6, 8, 9, 8, 8, 9, 
	20, 8, 21, 10, 11, 1, 12, 2, 
	13, 0, 14, 15, 11, 11, 19, 11, 
	17, 11, 12, 11, 11, 12, 12, 12, 
	12, 12, 12, 11, 11, 11, 11, 3, 
	11, 4, 5, 17, 11, 16, 11, 4, 
	17, 11, 18, 18, 18, 11, 6, 7, 
	11, 6, 0, 0, 11, 11, 11, 11, 
	11, 11, 11, 11, 11, 11, 11, 11, 
	11, 0
};

static const char _clang_trans_actions[] = {
	17, 0, 0, 15, 0, 44, 0, 0, 
	37, 0, 0, 0, 37, 1, 0, 19, 
	0, 1, 0, 1, 0, 0, 1, 0, 
	3, 0, 5, 0, 41, 0, 47, 0, 
	0, 0, 11, 11, 13, 13, 11, 13, 
	11, 13, 50, 13, 21, 50, 50, 50, 
	50, 50, 50, 39, 23, 27, 25, 0, 
	27, 0, 0, 11, 29, 0, 31, 0, 
	11, 29, 0, 0, 0, 33, 1, 0, 
	19, 0, 0, 0, 35, 37, 37, 35, 
	35, 39, 27, 27, 29, 31, 29, 33, 
	27, 0
};

static const char _clang_to_state_actions[] = {
	0, 0, 0, 0, 0, 0, 0, 0, 
	7, 0, 7, 7, 0, 0, 0, 0, 
	0, 0, 0, 0, 0, 0
};

static const char _clang_from_state_actions[] = {
	0, 0, 0, 0, 0, 0, 0, 0, 
	0, 0, 0, 9, 0, 0, 0, 0, 
	0, 0, 0, 0, 0, 0
};

static const char _clang_eof_trans[] = {
	0, 0, 0, 81, 79, 79, 81, 81, 
	0, 0, 0, 0, 82, 89, 89, 87, 
	86, 87, 88, 89, 0, 0
};

static const int clang_start = 11;
static const int clang_error = 0;

static const int clang_en_block_comment = 8;
static const int clang_en_line_comment = 10;
static const int clang_en_main = 11;


#line 133 "src/sqlscanner.rl"

#define BUFSIZE 128


int scanner(const char *sql)
{
    static char buf[BUFSIZE+1];
    int cs, act, have = 0, curline = 1;
    char *ts, *te = 0;
    int done = 0;
    int pointer = 0;
    int sqllen = strlen(sql);

    char arg[BUFSIZE+1] = {"\0"};

    initialize_fsm();

    
#line 148 "src/sqlscanner.c"
	{
	cs = clang_start;
	ts = 0;
	te = 0;
	act = 0;
	}

#line 151 "src/sqlscanner.rl"

    while ( !done ) {
        char *p = buf + have, *pe, *eof = 0;
        int len, space = BUFSIZE - have;
        
        if ( space == 0 ) {
            // We've used up the entire buffer storing an already-parsed token
            // prefix that must be preserved.
            printf("Out of buffer space!\n");
            PyErr_SetString(SqlineageError, "Out of buffer space.");
            return -1;
        }

        space = MIN(space, sqllen-pointer);
        strncpy(p, &sql[pointer], space);
        p[space] = '\0';
        // printf("\n\n%s\n", p);
        len = strlen(p);
        pointer += len;
        pe = p + len;

        // Check if this is the end of file.
        if ( pointer >= sqllen ) {
            eof = pe;
            done = 1;
        }

        
#line 185 "src/sqlscanner.c"
	{
	int _klen;
	unsigned int _trans;
	const char *_acts;
	unsigned int _nacts;
	const char *_keys;

	if ( p == pe )
		goto _test_eof;
	if ( cs == 0 )
		goto _out;
_resume:
	_acts = _clang_actions + _clang_from_state_actions[cs];
	_nacts = (unsigned int) *_acts++;
	while ( _nacts-- > 0 ) {
		switch ( *_acts++ ) {
	case 4:
#line 1 "NONE"
	{ts = p;}
	break;
#line 206 "src/sqlscanner.c"
		}
	}

	_keys = _clang_trans_keys + _clang_key_offsets[cs];
	_trans = _clang_index_offsets[cs];

	_klen = _clang_single_lengths[cs];
	if ( _klen > 0 ) {
		const char *_lower = _keys;
		const char *_mid;
		const char *_upper = _keys + _klen - 1;
		while (1) {
			if ( _upper < _lower )
				break;

			_mid = _lower + ((_upper-_lower) >> 1);
			if ( (*p) < *_mid )
				_upper = _mid - 1;
			else if ( (*p) > *_mid )
				_lower = _mid + 1;
			else {
				_trans += (unsigned int)(_mid - _keys);
				goto _match;
			}
		}
		_keys += _klen;
		_trans += _klen;
	}

	_klen = _clang_range_lengths[cs];
	if ( _klen > 0 ) {
		const char *_lower = _keys;
		const char *_mid;
		const char *_upper = _keys + (_klen<<1) - 2;
		while (1) {
			if ( _upper < _lower )
				break;

			_mid = _lower + (((_upper-_lower) >> 1) & ~1);
			if ( (*p) < _mid[0] )
				_upper = _mid - 2;
			else if ( (*p) > _mid[1] )
				_lower = _mid + 2;
			else {
				_trans += (unsigned int)((_mid - _keys)>>1);
				goto _match;
			}
		}
		_trans += _klen;
	}

_match:
_eof_trans:
	cs = _clang_trans_targs[_trans];

	if ( _clang_trans_actions[_trans] == 0 )
		goto _again;

	_acts = _clang_actions + _clang_trans_actions[_trans];
	_nacts = (unsigned int) *_acts++;
	while ( _nacts-- > 0 )
	{
		switch ( *_acts++ )
		{
	case 0:
#line 20 "src/sqlscanner.rl"
	{curline += 1;}
	break;
	case 1:
#line 24 "src/sqlscanner.rl"
	{{cs = 11; goto _again;}}
	break;
	case 2:
#line 25 "src/sqlscanner.rl"
	{{cs = 11; goto _again;}}
	break;
	case 5:
#line 1 "NONE"
	{te = p+1;}
	break;
	case 6:
#line 37 "src/sqlscanner.rl"
	{act = 1;}
	break;
	case 7:
#line 44 "src/sqlscanner.rl"
	{act = 2;}
	break;
	case 8:
#line 37 "src/sqlscanner.rl"
	{te = p+1;{
        // printf( "symbol(%i): %c\n", curline, ts[0] );
        push_symbol(ts[0]);
    }}
	break;
	case 9:
#line 58 "src/sqlscanner.rl"
	{te = p+1;{
/*
        printf( "single_lit(%i): ", curline );
        fwrite( ts, 1, te-ts, stdout );
        printf("\n");
*/
    }}
	break;
	case 10:
#line 68 "src/sqlscanner.rl"
	{te = p+1;{
/*
        printf( "double_lit(%i): ", curline );
        fwrite( ts, 1, te-ts, stdout );
        printf("\n");
*/
    }}
	break;
	case 11:
#line 78 "src/sqlscanner.rl"
	{te = p+1;{
        memset(arg, 0x00, BUFSIZE);
        strncpy(arg, ts, te-ts);    
/*
        printf( "backtick(%i): ", curline );
        fwrite(arg, 1, strlen(arg), stdout);
        printf("\n");
*/
        push_backtick_literal(arg);
    }}
	break;
	case 12:
#line 90 "src/sqlscanner.rl"
	{te = p+1;}
	break;
	case 13:
#line 95 "src/sqlscanner.rl"
	{te = p+1;}
	break;
	case 14:
#line 96 "src/sqlscanner.rl"
	{te = p+1;{ {cs = 10; goto _again;} }}
	break;
	case 15:
#line 97 "src/sqlscanner.rl"
	{te = p+1;{ {cs = 8; goto _again;} }}
	break;
	case 16:
#line 37 "src/sqlscanner.rl"
	{te = p;p--;{
        // printf( "symbol(%i): %c\n", curline, ts[0] );
        push_symbol(ts[0]);
    }}
	break;
	case 17:
#line 101 "src/sqlscanner.rl"
	{te = p;p--;{
/*
        printf( "int(%i): ", curline );
        fwrite( ts, 1, te-ts, stdout );
        printf("\n");
*/
    }}
	break;
	case 18:
#line 111 "src/sqlscanner.rl"
	{te = p;p--;{
/*
        printf( "float(%i): ", curline );
        fwrite( ts, 1, te-ts, stdout );
        printf("\n");
*/
    }}
	break;
	case 19:
#line 121 "src/sqlscanner.rl"
	{te = p;p--;{
/*
        printf( "hex(%i): ", curline );
        fwrite( ts, 1, te-ts, stdout );
        printf("\n");
*/
    }}
	break;
	case 20:
#line 37 "src/sqlscanner.rl"
	{{p = ((te))-1;}{
        // printf( "symbol(%i): %c\n", curline, ts[0] );
        push_symbol(ts[0]);
    }}
	break;
	case 21:
#line 101 "src/sqlscanner.rl"
	{{p = ((te))-1;}{
/*
        printf( "int(%i): ", curline );
        fwrite( ts, 1, te-ts, stdout );
        printf("\n");
*/
    }}
	break;
	case 22:
#line 1 "NONE"
	{	switch( act ) {
	case 1:
	{{p = ((te))-1;}
        // printf( "symbol(%i): %c\n", curline, ts[0] );
        push_symbol(ts[0]);
    }
	break;
	case 2:
	{{p = ((te))-1;}
        memset(arg, 0x00, BUFSIZE);
        strncpy(arg, ts, te-ts);

/*
        printf( "ident(%i): ", curline );
        fwrite(arg, 1, strlen(arg), stdout);
        printf("\n");
*/
        push_ident(arg);
    }
	break;
	}
	}
	break;
#line 430 "src/sqlscanner.c"
		}
	}

_again:
	_acts = _clang_actions + _clang_to_state_actions[cs];
	_nacts = (unsigned int) *_acts++;
	while ( _nacts-- > 0 ) {
		switch ( *_acts++ ) {
	case 3:
#line 1 "NONE"
	{ts = 0;}
	break;
#line 443 "src/sqlscanner.c"
		}
	}

	if ( cs == 0 )
		goto _out;
	if ( ++p != pe )
		goto _resume;
	_test_eof: {}
	if ( p == eof )
	{
	if ( _clang_eof_trans[cs] > 0 ) {
		_trans = _clang_eof_trans[cs] - 1;
		goto _eof_trans;
	}
	}

	_out: {}
	}

#line 179 "src/sqlscanner.rl"

        if ( cs == clang_error ) {
            printf("Error when parsing\n");
            PyErr_SetString(SqlineageError, "Error when parsing.");
            return -1;
        }

        if ( ts == 0 )
            have = 0;
        else {
            // There is a prefix to preserve, shift it over.
            have = pe - ts;
            memmove( buf, ts, have );
            te = buf + (te-ts);
            ts = buf;
        }
    }
    return 0;
}


static PyObject *
sqlineage_scan(PyObject *self, PyObject *args)
{
    const char *sql;
    PyObject *temp;
    PyObject *result = NULL;

    if (!PyArg_ParseTuple(args, "sO:set_callback", &sql, &temp))
        return NULL;

    if (!PyCallable_Check(temp)) {
        PyErr_SetString(PyExc_TypeError, "Callback parameter must be callable");
        return NULL;
    }
    Py_XINCREF(temp);      /* Add a reference to new callback */
    Py_XDECREF(callback);  /* Dispose of previous callback */
    callback = temp;       /* Remember new callback */

    if (scanner(sql) != 0) {
        return NULL;
    }

    send_model(callback);

    memory_cleanup();

    /* Boilerplate to return "None" */
    Py_INCREF(Py_None);
    result = Py_None;
    return result;
}

static PyMethodDef SqlineageMethods[] = {
    {"scan",  sqlineage_scan, METH_VARARGS, "Scan an SQL file"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef sqlineageModule =
{
    PyModuleDef_HEAD_INIT,
    "sqlineage", /* name of module */
    "",          /* module documentation, may be NULL */
    -1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    SqlineageMethods
};

PyMODINIT_FUNC PyInit_sqlineage(void)
{
    PyObject *m;

    m = PyModule_Create(&sqlineageModule);
    if (m == NULL)
        return NULL;

    SqlineageError = PyErr_NewException("sqlineage.error", NULL, NULL);
    Py_INCREF(SqlineageError);
    PyModule_AddObject(m, "error", SqlineageError);
    return m;
}
