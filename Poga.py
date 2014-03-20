#encoding:UTF-8

#position is opcode value and the tuple consists of name and length
INSTRUCTION = ( 
    ("INV", 1), ("WRITE_VAR", 1), ("PUSH_RETVAL", 1), ("INV", 1), ("OR", 1), ("AND", 1), ("CMP_NE", 1), ("CMP_EQ", 1), #07
    ("CMP_L", 1), ("GO_SUB", 1), ("END", 1), ("CMP_GE", 1), ("ADD", 1), ("SUB", 1), ("MUL", 1), ("DIV", 1),  #0F
    ("MOD", 1), ("CMP_EQ(BOOL)", 1), ("NEG", 1), ("SHL", 1), ("INC", 1), ("DEC", 1), ("RET", 1), ("READ_VAR", 1),  #17
    ("CMP_LE", 1), ("NOT", 1), ("CMP_G", 1), ("INV", 1), ("XOR", 1), ("INC", 1), ("DEC", 1), ("SHR", 1), #1F
    ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("CALL_NO", 2), ("INV", 1), ("INV", 1), ("INV", 1), #27
    ("CALL_NO", 3), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), #2F
    ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("PUSH_STR", 2), ("INV", 1), ("INV", 1), ("INV", 1), #37
    ("PUSH_STR", 3), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), #3F
    ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("DATA_DEF", 2), ("INV", 1), ("INV", 1), ("INV", 1), #47
    ("JUMP", 3), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), #4F
    ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("PUSH", 2), ("INV", 1), ("INV", 1), ("INV", 1), #57
    ("PUSH", 3), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), #5F
    ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("PUSH_VARADDR", 2), ("INV", 1), ("INV", 1), ("INV", 1), #67
    ("PUSH_FUNCADDR", 3), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), #6F
    ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("ASS_LOC", 2), ("INV", 1), ("INV", 1), ("INV", 1), #77
    ("ASS_LOC", 3), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), #7F
    ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("LOAD_LOCVAR", 2), ("INV", 1), ("INV", 1), ("INV", 1),  #87
    ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), #8F
    ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("LOAD_PARAM", 2), ("INV", 1), ("INV", 1), ("INV", 1), #97
    ("LOAD_PARAM", 3), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), #9F
    ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("LOAD_PARAM", 2), ("INV", 1), ("INV", 1), ("INV", 1), #A7
    ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), #AF
    ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("ASS_GLOB", 2), ("INV", 1), ("INV", 1), ("INV", 1), #B7
    ("ASS_GLOB", 3), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), #BF
    ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("LOAD_GLOVAR", 2), ("INV", 1), ("INV", 1), ("INV", 1), #C7
    ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), #CF
    ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("JUMP_ZNS", 2), ("INV", 1), ("INV", 1), ("INV", 1), #D7
    ("JUMP", 3), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), #DF
    ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("JUMP_ZS", 2), ("INV", 1), ("INV", 1), ("INV", 1), #E7
    ("JUMP_ZNS", 3), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), #EF
    ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), #0xF7
    ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1), ("INV", 1)) #FF
 
BUILTIN = { 
    #joystick  functions
    0xFFE6: "joystick", 0xFFE5: "joyval", 
    #memory access functions
    0xFFF5: "peekW", 0xFFF6: "peekB", 0xFFF3: "pokeW", 0xFFF4: "pokeB",
     #user stack functions
    0xFF9F: "setsp", 0xFF9E: "getsp", 0xFF9B: "push", 0xFF9D: "pop", 
    0xFF9C: "drop", 0xFF9B: "call", 0xFF9A: "exec", 
    #math functions
    0xFFEB: "SEED", 0xFFEC: "RAND", 0xFFF1: "MIN", 0xFFF0: "MAX", 
    0xFFE9: "SQRT", 0xFFEA: "OVF", 0xFFEE: "SIN", 0xFFED: "COS", 
    #text and string function
    0xFF94: "strwidth", 0xFF93: "strheight", 0xFF97: "strlen", 0xFF96: "charwidth", 
    0xFF95: "charheight",  0xFFF9: "print", 0xFFF7: "putstr", 0xFFFE: "putch",
    0xFF74: "txt_MoveCursor", 0xFFFB: "to", 0xFFE7: "txt_Set", 0xFF7F: "txt_FGcolour",
    0xFF7C: "txt_Height", 0xFF7B: "txt_Width", 0xFF76: "txt_Bold", 0xFF75: "txt_Italic",
    #: "putnum", 
    #graphic functions
    0xFFE2: "gfx_Cls", 0xFFC9: "gfx_ChangeColour", 0xFFD8: "gfx_Circle", 0xFFD7: "gfx_CircleFilled", 
    0xFFDD: "gfx_Line", 0xFFDB: "gfx_Hline", 0xFFCE: "gfx_Vline", 0xFFDA: "gfx_Rectangle",
    0xFFD9: "gfx_RectangleFilled", 0xFFD1: "gfx_Polyline", 0xFFD0: "gfx_Polygon", 0xFFD4: "gfx_Triangle",
    0xFFD5: "gfx_Dot", 0xFFCF: "gfx_Bullet", 0xFFD3: "gfx_OrbitInit", 0xFFD2: "gfx_Orbit", 
    0xFFDE: "gfx_PutPixel", 0xFFD6: "gfx_GetPixel", 0xFFE1: "gfx_MoveTo", 0xFFC8: "gfx_MoveRel", 
    0xFFCB: "gfx_LineTo", 0xFFDF: "gfx_LineRel", 0xFFCA: "gfx_BoxTo", 0xFFC7: "gfx_SetClipRegion", 
    0xFFE0: "gfx_ClipWindow", 0xFFCD: "gfx_SpriteSet", 0xFFCC: "gfx_BlitSprite", 
    0xFFE3: "gfx_Set",0xFF91: "rect_Within", 0xFF92: "rect_Intersect", #no function call "gfx_FocusWindow",
    #display i/o functions
    0xFFA7: "disp_setGRAM", 0xFFAD: "disp_WriteControl", 0xFFAE: "disp_WriteByte", 0xFFAC: "disp_WrGRAM", 
    0xFFAB: "disp_ReadByte", 0xFFAA: "disp_RdGRAM", 0xFFA9: "disp_BlitPixelFill", 0xFFA8: "disp_BlitPixelsToMedia", 
    0xFFA4: "disp_BlitPixelsFromMedia",
    #media functions
    0xFFC5: "media_SetAdd",  0xFFC4: "media_SetSector", 0xFFB6: "media_Init",
    0xFFC0: "media_ReadByte", 0xFFBF: "media_ReadWord", 0xFFBE: "media_WriteByte", 0xFFBD: "media_WriteWord", 
    0xFFB7: "media_Flush", 0xFFBC: "media_Image", 0xFFBB: "media_Video", 0xFFBA: "media_VideoFrame",
    0xFFC6: "media_SelectGCIimage", 0xFFC3: "media_Offset", 0xFFC2: "media_LoadArray", 0xFFC1: "media_StoreArray",
    0xFFB9: "media_LoadImageHeader", 0xFFB8: "media_SetScanLine", 0xFFB7: "media_Flush", 0xFFB5: "media_PoGaFile", 
    #PoGa File System Operations
    0xFFA1: "RunProgram", 0xFFA0: "LoadProgram",
    #extended functions
    0xFF80: "EVE_SP", 0xFF98: "iterator",
    #serial communication functions
    0xFFFF: "serin", 0xFFFD: "serout", 0xFFFC: "setbaud", 0xFF8E: "com_Init",
    0xFF8D: "com_Reset", 0xFF8C: "com_Count", 0xFF8B: "com_Full", 0xFF8A: "com_Error", 
    0xFF89: "com_Sync", 0xFF88: "com_TX", 0xFF86: "com_CSUM_8", 0xFF85: "com_CRC_16", 
    0xFF84: "com_MODBUS", 0xFF83: "com_CRC_CCITT", 0xFF82: "sys_EventsPostpone",  0xFF81: "sys_EventsResume",
    #sound functions
    0xFFE4: "beep", 0xFFB4: "tune_Play", 0xFFAF: "tune_Playing", 0xFFB3: "tune_Pause", 
    0xFFB2: "tune_Continue", 0xFFB0: "tune_End", 0xFFB1: "tune_Stop",
    #general purpose functions
    0xFFF8: "lookup", 0xFFFA: "pause"
}  

def zeroleaded_hex_str(byte_sequence):
    '''creates hex string from character list'''
    return "".join(map(lambda x: "%02X" % ord(x), byte_sequence))