#ifndef OLED_UI_ASSETS_H
#define OLED_UI_ASSETS_H
#include <stdint.h>
typedef struct {uint8_t width,height;uint16_t rows[12];} UiGlyph;
typedef struct {uint16_t length;const int16_t *tokens;} UiText;
typedef struct {int16_t kind,x,y,w,h,ref;} UiElement;
typedef struct {uint16_t first,count;} UiPage;
typedef struct {int16_t kind,target;int32_t value;} UiAction;
typedef struct {int16_t x,y,w,h,title,variable,number;int32_t minimum,maximum,step;UiAction confirm,cancel;} UiDialog;
extern const UiGlyph ui_glyphs[];
extern const UiText ui_texts[];
extern const UiElement ui_elements[];
extern const UiPage ui_pages[];
extern const UiDialog ui_dialogs[];
extern const UiAction ui_bindings[][6];
extern const uint8_t *const ui_images[];
extern const int32_t ui_initial[];
extern const uint16_t ui_digits[10];
#define UI_VAR_COUNT 1u
#define UI_VAR_STORAGE 1u
#define UI_PAGE_COUNT 1u
#define UI_START_PAGE 0u
#define UI_MINUS 10u
#define UI_DIALOG_FOOTER 0u
#define UI_VAR_0 0u
#endif
