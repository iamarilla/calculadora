_BASE = """
QPushButton {{
    border-radius: 10px; font-size: 18px; font-weight: bold;
    min-width: 64px; min-height: 56px;
}}
.btn_num   {{ background-color: {num};   color: {txt}; }}
.btn_num:hover    {{ background-color: {num_h}; }}
.btn_num:pressed  {{ background-color: {num_p}; }}
.btn_op    {{ background-color: {num};   color: {acc}; }}
.btn_op:hover     {{ background-color: {num_h}; }}
.btn_op:pressed   {{ background-color: {num_p}; }}
.btn_func  {{ background-color: {num};   color: {sub}; }}
.btn_func:hover   {{ background-color: {num_h}; }}
.btn_func:pressed {{ background-color: {num_p}; }}
.btn_igual {{ background-color: {acc};   color: {bg}; }}
.btn_igual:hover  {{ background-color: {acc_h}; }}
.btn_igual:pressed{{ background-color: {acc_p}; }}
.btn_clear {{ background-color: transparent; color: {red}; }}
.btn_clear:hover  {{ background-color: {red_bg}; }}
.btn_clear:pressed{{ background-color: {red_bg2}; }}
.btn_back  {{ background-color: {num};   color: {red}; }}
.btn_back:hover   {{ background-color: {num_h}; }}
.btn_back:pressed {{ background-color: {num_p}; }}
.btn_paren {{ background-color: {num};   color: {teal}; }}
.btn_paren:hover  {{ background-color: {num_h}; }}
.btn_paren:pressed{{ background-color: {num_p}; }}
.btn_sci {{
    background-color: {sci_bg}; color: {blue};
    border: 1px solid {border};
    min-width: 52px; min-height: 38px;
    font-size: 13px; border-radius: 8px; font-weight: bold;
}}
.btn_sci:hover  {{ background-color: {sci_h}; border-color: {border_h}; }}
.btn_sci:pressed{{ background-color: {num}; }}
.btn_modo {{
    background-color: {num}; color: {green};
    min-width: 48px; min-height: 26px; max-height: 26px;
    font-size: 11px; border-radius: 6px; font-weight: bold;
}}
.btn_modo:hover  {{ background-color: {num_h}; }}
.btn_modo:pressed{{ background-color: {num_p}; }}
.btn_tema {{
    background-color: {num}; color: {yellow};
    min-width: 28px; min-height: 26px; max-height: 26px;
    font-size: 14px; border-radius: 6px; padding: 0;
}}
.btn_tema:hover  {{ background-color: {num_h}; }}
.btn_tema:pressed{{ background-color: {num_p}; }}
"""


def _tema(dark: bool) -> str:
    if dark:
        v = dict(
            bg="#1e1e2e", surf="#181825", border="#313244", border_h="#45475a",
            txt="#cdd6f4", sub="#a6adc8", hint="#585b70",
            acc="#cba6f7", acc_h="#d0bcff", acc_p="#b796f0",
            red="#f38ba8", red_bg="#2a1e2e", red_bg2="#3a2030",
            teal="#89dceb", blue="#89b4fa", green="#a6e3a1", yellow="#f9e2af",
            num="#313244", num_h="#45475a", num_p="#585b70",
            sci_bg="#1e1e2e", sci_h="#2a2a3e",
            sel_bg="#45475a", sel_fg="#cba6f7",
            sep="#313244",
        )
    else:
        v = dict(
            bg="#eff1f5", surf="#e6e9ef", border="#ccd0da", border_h="#bcc0cc",
            txt="#4c4f69", sub="#6c6f85", hint="#acb0be",
            acc="#8839ef", acc_h="#7527df", acc_p="#6316cf",
            red="#d20f39", red_bg="#fce8ec", red_bg2="#f9d0d8",
            teal="#179299", blue="#1e66f5", green="#40a02b", yellow="#df8e1d",
            num="#dce0e8", num_h="#ccd0da", num_p="#bcc0cc",
            sci_bg="#eff1f5", sci_h="#e6e9ef",
            sel_bg="#ccd0da", sel_fg="#8839ef",
            sep="#ccd0da",
        )
    return f"""
QWidget {{
    background-color: {v['bg']};
    color: {v['txt']};
    font-family: 'Inter', 'Segoe UI', sans-serif;
}}
#panel_hist {{
    background-color: {v['surf']};
    border-right: 1px solid {v['border']};
}}
#titulo_hist {{ color: {v['acc']}; font-size: 13px; font-weight: bold; }}
#btn_borrar {{
    color: {v['red']}; background: transparent;
    border: none; font-size: 11px; padding: 2px 6px;
}}
#btn_borrar:hover {{ color: {v['acc_h']}; }}
#lista_hist {{
    background-color: {v['surf']}; border: none;
    font-size: 12px; color: {v['txt']};
}}
#lista_hist::item {{ padding: 6px 10px; border-radius: 6px; }}
#lista_hist::item:selected {{ background-color: {v['border']}; color: {v['acc']}; }}
#lista_hist::item:hover {{ background-color: {v['sci_h']}; }}
#hint {{ color: {v['hint']}; font-size: 9px; padding: 4px 10px 8px 10px; }}
#sep, #sep2 {{ background-color: {v['sep']}; }}
#lbl_histlinea {{ color: {v['hint']}; font-size: 13px; padding-right: 6px; }}
QLineEdit#lbl_display {{
    color: {v['txt']};
    background: transparent;
    border: none;
    padding: 0 8px 0 0;
    selection-background-color: {v['sel_bg']};
    selection-color: {v['sel_fg']};
}}
{_BASE.format(**v)}"""


TEMAS: dict[str, str] = {
    "oscuro": _tema(True),
    "claro":  _tema(False),
}
