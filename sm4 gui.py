#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog
import tkinter as tk

import customtkinter as ctk
from customtkinter import (
    CTkLabel,
    CTkButton,
    CTkEntry,
    CTkTextbox,
    CTkFrame,
    CTkSegmentedButton,
    CTkScrollableFrame,
)

from sm4_core import (
    sm4_encrypt_ecb,
    sm4_decrypt_ecb,
    generate_key,
    load_key_hex,
    load_key,
    SM4,
    parse_hex_string,
    format_hex_block,
)

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


# ==================== МУЛЬТИМОВНІСТЬ ====================
TRANSLATIONS = {
    "ua": {
        # Загальні
        "title": "🔐 Утиліта шифрування/дешифрування SM4",
        "subtitle": "Безпечне шифрування текстів та файлів за стандартом SM4",
        "files_tab": "📁 Файли",
        "text_tab": "📝 Текст",
        "footer": "© 2025 by Roman Sadovskyi  •  SM4 ECB Mode Utility",
        
        # Вкладка Текст
        "about_program": "▶ Про програму",
        "about_program_expanded": "▼ Про програму",
        "how_it_works": "▶ Як це працює?",
        "how_it_works_expanded": "▼ Як це працює?",
        "input_text": "📝 Вхідний текст",
        "encryption_key": "🔑 Ключ шифрування",
        "result": "📤 Результат",
        "generate_key": "🎲 Згенерувати новий ключ",
        "encrypt": "🔒 Зашифрувати",
        "decrypt": "🔓 Розшифрувати",
        "paste": "📋 Вставити",
        "paste_key": "📋 Вставити ключ",
        "copy": "📋 Копіювати",
        "clear": "🗑️ Очистити",
        "key_placeholder": "Введіть або згенеруйте ключ (32 HEX)",
        
        # Вкладка Файли
        "whole_file": "Файл цілком",
        "content_only": "Лише вміст (.txt)",
        "select_file_encrypt": "📂 Вибрати файл для шифрування",
        "select_file_decrypt": "📂 Вибрати файл для розшифрування",
        "select_key_file": "🔑 Вибрати файл-ключ",
        "generate_key_file": "🎲 Згенерувати ключ у файл",
        "encrypt_file": "🔒 Зашифрувати файл",
        "decrypt_file": "🔓 Розшифрувати файл",
        "no_file_selected": "📎 Файл не обрано",
        "no_key_selected": "Ключ не вибрано",
        "file_selection": "📁 Вибір файлу",
        "key_management": "🔑 Управління ключем",
        "select_file": "📂 Обрати файл",
        "generate_key_btn": "🎲 Згенерувати ключ",
        "load_key_btn": "📂 Завантажити ключ",
        "mode_label": "Режим:",
        "padding_none": "Немає",
        
        # Підказки
        "tooltip_input": "Вводьте будь-який текст. Довжина не обмежена.",
        "tooltip_key": "Ключ має містити рівно 32 HEX-символи (0–9, a–f).\nПриклад: 0123456789abcdef0123456789abcdef.\nНатисніть «Згенерувати» для випадкового ключа.",
        "tooltip_result": "Результат шифрування/розшифрування відображається тут.",
        "tooltip_paste": "Вставити текст із буфера обміну (Ctrl+V).",
        "tooltip_paste_key": "Вставити ключ із буфера обміну (Ctrl+V).",
        "tooltip_copy": "Копіювати результат у буфер обміну (Ctrl+C).",
        "tooltip_clear": "Очистити поле результату.",
        "tooltip_generate_key": "Створити випадковий 128-бітний ключ.",
        "tooltip_encrypt": "Зашифрувати текст за алгоритмом SM4 (ECB).",
        "tooltip_decrypt": "Розшифрувати HEX-шифртекст у початковий текст.",
        "tooltip_padding": "Перемикач доповнення (Текст):\n • PKCS#7 — авто-доповнення до 16 байт\n • Немає — без доповнення (кратно 16).",
        
        # Повідомлення
        "success": "✅ Успішно",
        "error": "❌ Помилка",
        "warning": "⚠️ Попередження",
        "key_generated": "Ключ успішно згенеровано",
        "copied_to_clipboard": "Скопійовано в буфер обміну",
        "no_text_to_copy": "Немає тексту для копіювання",
        "invalid_name": "Некоректна назва",
        "invalid_name_msg": "Перевірте, що назва не порожня і не містить заборонених символів.",
        "confirm": "✅ Підтвердити",
        "cancel": "✖ Скасувати",
        
        # Інфо тексти
        "about_program_title": "ℹ️ Про програму",
        "how_it_works_title": "ℹ️ Як користуватися режимом «Текст»",
        "how_it_works_files_title": "ℹ️ Як користуватися режимом «Файли»",
        
        # Довгі тексти
        "about_text": (
            "📋 Утиліта для шифрування/розшифрування за алгоритмом SM4 у режимі ECB.\n\n"
            "🔧 Режими роботи:\n"
            "  • Текст — шифрування/розшифрування рядків з вибором формату введення.\n"
            "  • Файли — шифрування всього файлу або лише текстового вмісту .txt. У режимі вмісту дані читаються/записуються як HEX-рядок.\n\n"
            "📝 Введення та ключ:\n"
            "  • Текст: звичайний текст (UTF-8) або HEX-рядок.\n"
            "  • Ключ: 32 HEX-символи або рівно 16 байтів тексту (UTF-8).\n"
            "  • У режимі «Лише вміст (.txt)» ключові файли також повинні бути .txt.\n"
            "  • Для .txt вмісту можна обрати формат: HEX-рядок шифрується напряму, текст (UTF-8) спершу переводиться у HEX.\n"
            "  • Результат у режимі Текст: шифртекст показується у HEX; для розшифрування вставте його назад.\n\n"
            "🧩 Доповнення (Padding):\n"
            "  • PKCS#7 — підходить для довільної довжини даних, автоматично доповнює до 16 байтів.\n"
            "  • Немає — довжина даних/шифртексту має бути кратною 16 байтам (зручно для тест-векторів).\n\n"
            "📦 Вивід у режимі Файли:\n"
            "  • Шифрування: файл зберігається як FILENAME_encrypted. У режимі вмісту зберігається читабельний HEX-рядок у .txt.\n"
            "  • Розшифрування: якщо ім'я має суфікс '_encrypted', відновлюється вихідна назва; інакше додається '_decrypted'. У режимі вмісту — HEX-рядок у .txt.\n\n"
            "ℹ️ Покрокові інструкції та підказки дивіться у розділі «Як це працює?» у кожній вкладці."
        ),
        "how_it_works_text": (
            "① Введіть або вставте текст у поле «Вхідний текст».\n\n"
            "② Оберіть формат введення: 'text' або 'hex' для тексту, та 'hex' або 'text' для ключа.\n\n"
            "③ Задайте ключ: введіть 32 HEX-символи (або рівно 16 байтів тексту) АБО натисніть «Згенерувати новий ключ».\n\n"
            "④ Натисніть «Зашифрувати» — у нижньому полі з'явиться шифртекст (у HEX-форматі).\n\n"
            "⑤ Для розшифрування вставте шифртекст у поле «Вхідний текст»,\n"
            "   вкажіть той самий ключ і натисніть «Розшифрувати».\n\n"
            "⑥ Режим ECB шифрує кожен блок по 16 байтів незалежно.\n\n"
            "🔧 Доповнення (Padding): оберіть 'PKCS#7' для довільної довжини або 'Немає' для довжини кратної 16; 'Немає' використовуйте для тест-векторів SM4."
        ),
        "how_it_works_files": (
            "① Оберіть режим: «Файл цілком» або «Лише вміст (.txt)». У режимі вмісту дозволені тільки .txt файли; ключовий файл також .txt.\n"
            "   У режимі вмісту вміст .txt трактуємо як HEX-рядок (пробіли/переноси допускаються). Шифрування/розшифрування працює напряму з HEX.\n\n"
            "② Оберіть файл відповідно до режиму (у режимі вмісту — лише .txt).\n\n"
            "③ Задайте ключ: згенеруйте новий або завантажте з файлу (у режимі вмісту — тільки .txt з HEX-ключем).\n\n"
            "④ Натисніть «Зашифрувати файл». Результат буде збережено як FILENAME_encrypted: у режимі вмісту — читабельний HEX-рядок у .txt.\n\n"
            "⑤ Для розшифрування оберіть зашифрований файл, переконайтеся у правильному ключі і натисніть «Розшифрувати файл».\n"
            "   У режимі вмісту після розшифрування у .txt записується читабельний HEX-рядок (без «сміття»).\n\n"
            "🔧 Доповнення (Padding):\n"
            "   • PKCS#7 — автоматично доповнює дані до 16 байтів; зручно для довільних файлів.\n"
            "   • Немає — без доповнення; довжина повинна бути кратною 16; підходить для тест-векторів SM4.\n\n"
            "⚠️ Якщо ключ буде іншим, файл не вдасться коректно розшифрувати."
        ),
    },
    "en": {
        # General
        "title": "🔐 SM4 Encryption/Decryption Utility",
        "subtitle": "Secure encryption of texts and files using SM4 standard",
        "files_tab": "📁 Files",
        "text_tab": "📝 Text",
        "footer": "© 2025 by Roman Sadovskyi  •  SM4 ECB Mode Utility",
        
        # Text Tab
        "about_program": "▶ About Program",
        "about_program_expanded": "▼ About Program",
        "how_it_works": "▶ How It Works?",
        "how_it_works_expanded": "▼ How It Works?",
        "input_text": "📝 Input Text",
        "encryption_key": "🔑 Encryption Key",
        "result": "📤 Result",
        "generate_key": "🎲 Generate New Key",
        "encrypt": "🔒 Encrypt",
        "decrypt": "🔓 Decrypt",
        "paste": "📋 Paste",
        "paste_key": "📋 Paste Key",
        "copy": "📋 Copy",
        "clear": "🗑️ Clear",
        "key_placeholder": "Enter or generate key (32 HEX)",
        
        # Files Tab
        "whole_file": "Whole File",
        "content_only": "Content Only (.txt)",
        "select_file_encrypt": "📂 Select File to Encrypt",
        "select_file_decrypt": "📂 Select File to Decrypt",
        "select_key_file": "🔑 Select Key File",
        "generate_key_file": "🎲 Generate Key to File",
        "encrypt_file": "🔒 Encrypt File",
        "decrypt_file": "🔓 Decrypt File",
        "no_file_selected": "📎 No file selected",
        "no_key_selected": "No key selected",
        "file_selection": "📁 File Selection",
        "key_management": "🔑 Key Management",
        "select_file": "📂 Select File",
        "generate_key_btn": "🎲 Generate Key",
        "load_key_btn": "📂 Load Key",
        "mode_label": "Mode:",
        "padding_none": "None",
        
        # Tooltips
        "tooltip_input": "Enter any text. Length is unlimited.",
        "tooltip_key": "Key must contain exactly 32 HEX characters (0–9, a–f).\nExample: 0123456789abcdef0123456789abcdef.\nClick 'Generate' for random key.",
        "tooltip_result": "Encryption/decryption result is displayed here.",
        "tooltip_paste": "Paste text from clipboard (Ctrl+V).",
        "tooltip_paste_key": "Paste key from clipboard (Ctrl+V).",
        "tooltip_copy": "Copy result to clipboard (Ctrl+C).",
        "tooltip_clear": "Clear result field.",
        "tooltip_generate_key": "Generate random 128-bit key.",
        "tooltip_encrypt": "Encrypt text using SM4 algorithm (ECB).",
        "tooltip_decrypt": "Decrypt HEX ciphertext to original text.",
        "tooltip_padding": "Padding switcher (Text):\n • PKCS#7 — auto-padding to 16 bytes\n • None — no padding (multiple of 16).",
        
        # Messages
        "success": "✅ Success",
        "error": "❌ Error",
        "warning": "⚠️ Warning",
        "key_generated": "Key successfully generated",
        "copied_to_clipboard": "Copied to clipboard",
        "no_text_to_copy": "No text to copy",
        "invalid_name": "Invalid Name",
        "invalid_name_msg": "Check that the name is not empty and does not contain forbidden characters.",
        "confirm": "✅ Confirm",
        "cancel": "✖ Cancel",
        
        # Info texts
        "about_program_title": "ℹ️ About Program",
        "how_it_works_title": "ℹ️ How to Use «Text» Mode",
        "how_it_works_files_title": "ℹ️ How to Use «Files» Mode",
        
        # Long texts
        "about_text": (
            "📋 Utility for encryption/decryption using SM4 algorithm in ECB mode.\n\n"
            "🔧 Operation Modes:\n"
            "  • Text — encrypt/decrypt strings with input format selection.\n"
            "  • Files — encrypt entire file or text content of .txt only. In content mode, data is read/written as HEX string.\n\n"
            "📝 Input and Key:\n"
            "  • Text: plain text (UTF-8) or HEX string.\n"
            "  • Key: 32 HEX characters or exactly 16 bytes of text (UTF-8).\n"
            "  • In 'Content Only (.txt)' mode, key files must also be .txt.\n"
            "  • For .txt content, you can choose format: HEX string is encrypted directly, text (UTF-8) is converted to HEX first.\n"
            "  • Result in Text mode: ciphertext shown in HEX; paste it back for decryption.\n\n"
            "🧩 Padding:\n"
            "  • PKCS#7 — suitable for arbitrary data length, automatically pads to 16 bytes.\n"
            "  • None — data/ciphertext length must be multiple of 16 bytes (useful for test vectors).\n\n"
            "📦 Output in Files Mode:\n"
            "  • Encryption: file saved as FILENAME_encrypted. In content mode, readable HEX string saved in .txt.\n"
            "  • Decryption: if name has '_encrypted' suffix, original name is restored; otherwise '_decrypted' is added. In content mode — HEX string in .txt.\n\n"
            "ℹ️ See step-by-step instructions and hints in 'How It Works?' section in each tab."
        ),
        "how_it_works_text": (
            "① Enter or paste text into 'Input Text' field.\n\n"
            "② Choose input format: 'text' or 'hex' for text, and 'hex' or 'text' for key.\n\n"
            "③ Set key: enter 32 HEX characters (or exactly 16 bytes of text) OR click 'Generate New Key'.\n\n"
            "④ Click 'Encrypt' — ciphertext will appear in bottom field (in HEX format).\n\n"
            "⑤ To decrypt, paste ciphertext into 'Input Text' field,\n"
            "   specify same key and click 'Decrypt'.\n\n"
            "⑥ ECB mode encrypts each 16-byte block independently.\n\n"
            "🔧 Padding: choose 'PKCS#7' for arbitrary length or 'None' for length multiple of 16; use 'None' for SM4 test vectors."
        ),
        "how_it_works_files": (
            "① Choose mode: 'Whole File' or 'Content Only (.txt)'. In content mode, only .txt files allowed; key file also .txt.\n"
            "   In content mode, .txt content treated as HEX string (spaces/newlines allowed). Encryption/decryption works directly with HEX.\n\n"
            "② Select file according to mode (in content mode — only .txt).\n\n"
            "③ Set key: generate new or load from file (in content mode — only .txt with HEX key).\n\n"
            "④ Click 'Encrypt File'. Result will be saved as FILENAME_encrypted: in content mode — readable HEX string in .txt.\n\n"
            "⑤ To decrypt, select encrypted file, ensure correct key and click 'Decrypt File'.\n"
            "   In content mode, after decryption, readable HEX string written to .txt (no garbage).\n\n"
            "🔧 Padding:\n"
            "   • PKCS#7 — automatically pads data to 16 bytes; convenient for arbitrary files.\n"
            "   • None — no padding; length must be multiple of 16; suitable for SM4 test vectors.\n\n"
            "⚠️ If key is different, file cannot be correctly decrypted."
        ),
    }
}


def create_tooltip(widget, text: str):
    tooltip_window = [None]

    def on_enter(event):
        if tooltip_window[0] is None:
            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = CTkLabel(
                tooltip,
                text=text,
                text_color="white",
                fg_color="#333333",
                corner_radius=4,
                padx=8,
                pady=4,
                font=("Segoe UI", 9),
            )
            label.pack()
            tooltip_window[0] = tooltip

    def on_leave(event):
        if tooltip_window[0] is not None:
            tooltip_window[0].destroy()
            tooltip_window[0] = None

    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)


class SM4App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("🔐 SM4 Encryption")
        self.geometry("1000x650")
        self.minsize(800, 550)

        # Language
        self.current_lang = "ua"  # Default language
        
        # Colors
        self.accent_color = "#0078D4"
        self.bg_color = "#F5F5F5"
        self.text_color = "#1F1F1F"
        self.info_color = "#E8F4F8"
        # Restore brighter palette
        self.success_color = "#27AE60"
        self.warning_color = "#FF9800"
        self.primary_soft = self.accent_color
        self.primary_soft_hover = "#005A9E"
        self.secondary_soft = self.warning_color
        self.secondary_soft_hover = "#E68900"
        self.paste_soft = "#D9ECFF"
        self.paste_soft_hover = "#BBD9FF"

        self.enc_file: Path | None = None
        self.enc_key: bytes | None = None
        # Шляхи користувача більше не задаються кнопками; вибір виконується під час дії
        self.show_text_info = False
        self.show_file_info = False
        self.show_prog_info_text = False
        self.show_prog_info_file = False
        # file_process_mode буде ініціалізовано після встановлення мови
        self.file_process_mode = None
        self.content_data_format = "hex"  # text | hex (for content-only mode)
        self._prev_file_process_mode = None

        self.about_text_common = TRANSLATIONS[self.current_lang]["about_text"]
        
        # Ініціалізуємо file_process_mode з перекладом
        self.file_process_mode = ctk.StringVar(value=self.t("whole_file"))
        self._prev_file_process_mode = self.t("whole_file")

        self._build_ui()

    def t(self, key: str) -> str:
        """Get translation for the current language."""
        return TRANSLATIONS[self.current_lang].get(key, key)
    
    def is_content_mode(self) -> bool:
        """Check if currently in content-only mode."""
        current = self.file_process_mode.get()
        return current == self.t("content_only") or current == "Лише вміст (.txt)" or current == "Content Only (.txt)"
    
    def switch_language(self):
        """Switch between Ukrainian and English."""
        self.current_lang = "en" if self.current_lang == "ua" else "ua"
        self.update_file_mode_values()
        self._rebuild_ui()
    
    def update_file_mode_values(self):
        """Update file mode dropdown values based on current language."""
        current_mode = self.file_process_mode.get()
        if self.current_lang == "en":
            if current_mode == "Файл цілком":
                self.file_process_mode.set("Whole File")
                self._prev_file_process_mode = "Whole File"
            elif current_mode == "Лише вміст (.txt)":
                self.file_process_mode.set("Content Only (.txt)")
                self._prev_file_process_mode = "Content Only (.txt)"
        else:
            if current_mode == "Whole File":
                self.file_process_mode.set("Файл цілком")
                self._prev_file_process_mode = "Файл цілком"
            elif current_mode == "Content Only (.txt)":
                self.file_process_mode.set("Лише вміст (.txt)")
                self._prev_file_process_mode = "Лише вміст (.txt)"
    
    def _rebuild_ui(self):
        """Rebuild UI with new language."""
        for widget in self.winfo_children():
            widget.destroy()
        self.about_text_common = TRANSLATIONS[self.current_lang]["about_text"]
        self.show_text_info = False
        self.show_file_info = False
        self.show_prog_info_text = False
        self.show_prog_info_file = False
        self._build_ui()

    # ============================ БАЗОВИЙ ІНТЕРФЕЙС ============================

    def _build_ui(self) -> None:
        main = CTkFrame(self, fg_color=self.bg_color)
        main.pack(fill="both", expand=True, padx=20, pady=20)


        header = CTkFrame(main, fg_color=self.bg_color)
        header.pack(fill="x", pady=(0, 15))

        title_frame = CTkFrame(header, fg_color=self.bg_color)
        title_frame.pack(side="left", fill="x", expand=True)

        title = CTkLabel(
            title_frame,
            text=self.t("title"),
            font=("Segoe UI", 28, "bold"),
            text_color=self.text_color,
        )
        title.pack(anchor="w")

        subtitle = CTkLabel(
            title_frame,
            text=self.t("subtitle"),
            font=("Segoe UI", 11, "bold"),
            text_color="#555555",
        )
        subtitle.pack(anchor="w", pady=(4, 0))

        # Language switcher button
        lang_btn = CTkButton(
            header,
            text="🌐 EN" if self.current_lang == "ua" else "🌐 UA",
            command=self.switch_language,
            fg_color="#9C27B0",
            hover_color="#7B1FA2",
            font=("Segoe UI", 11, "bold"),
            width=80,
            height=35,
            corner_radius=8,
        )
        lang_btn.pack(side="right", padx=(8, 0), pady=8)

        self.mode_var = ctk.StringVar(value=self.t("files_tab"))
        segmented = CTkSegmentedButton(
            header,
            values=[self.t("files_tab"), self.t("text_tab")],
            variable=self.mode_var,
            command=self._on_mode_change,
            font=("Segoe UI", 12, "bold"),
            fg_color=self.bg_color,
            selected_color="#2E7DD7",
            selected_hover_color="#266CC0",
            unselected_color="#D0D0D0",
            unselected_hover_color="#C5C5C5",
            corner_radius=10,
        )
        segmented.pack(side="right", padx=(0, 12), pady=8)

        self.padding_mode_global = ctk.StringVar(value="PKCS#7")

        self.content = CTkScrollableFrame(main, fg_color=self.bg_color)
        self.content.pack(fill="both", expand=True)

        self.text_frame = CTkFrame(self.content, fg_color=self.bg_color)
        self.file_frame = CTkFrame(self.content, fg_color=self.bg_color)

        self._build_text_tab()
        self._build_file_tab()
        self._on_mode_change()

        footer = CTkFrame(main, fg_color=self.bg_color, height=30)
        footer.pack(fill="x", pady=(10, 0), side="bottom")

        footer_label = CTkLabel(
            footer,
            text=self.t("footer"),
            font=("Segoe UI", 12),
            text_color="#999999",
        )
        footer_label.pack(anchor="center", padx=5, pady=2)


    def _prompt_name_modal(self, title: str, message: str, initial: str) -> str | None:
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("520x230")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        dialog.configure(fg_color="white")

        container = CTkFrame(dialog, fg_color="white")
        container.pack(fill="both", expand=True, padx=16, pady=14)

        lbl = CTkLabel(container, text=message, font=("Segoe UI", 13, "bold"), text_color=self.text_color)
        lbl.pack(anchor="w")

        var = tk.StringVar(value=initial)
        entry = CTkEntry(
            container,
            textvariable=var,
            font=("Courier New", 14, "bold"),
            fg_color="white",
            border_color="#C8C8C8",
            border_width=1,
            corner_radius=10,
        )
        entry.pack(fill="x", pady=(8, 8))
        entry.focus_set()

        hint = CTkLabel(container, text="Без заборонених символів шляху: \\ / : * ? \" < > |", font=("Segoe UI", 10), text_color="#666666")
        hint.pack(anchor="w", pady=(0, 12))

        result = {"name": None}

        def is_valid(name: str) -> bool:
            bad = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
            return bool(name) and not any(ch in name for ch in bad)

        def on_ok():
            name = var.get().strip()
            if not is_valid(name):
                messagebox.showerror("Некоректна назва", "Перевірте, що назва не порожня і не містить заборонених символів.")
                return
            result["name"] = name
            dialog.destroy()

        def on_cancel():
            result["name"] = None
            dialog.destroy()

        btns = CTkFrame(container, fg_color="white")
        btns.pack(fill="x")

        ok_btn = CTkButton(
            btns,
            text="✅ Підтвердити",
            command=on_ok,
            fg_color=self.accent_color,
            hover_color="#005A9E",
            font=("Segoe UI", 12, "bold"),
            height=38,
            corner_radius=8,
        )
        ok_btn.pack(side="left", expand=True, fill="x", padx=(0, 8))

        cancel_btn = CTkButton(
            btns,
            text="✖ Скасувати",
            command=on_cancel,
            fg_color="#E0E0E0",
            hover_color="#CFCFCF",
            text_color="#333333",
            font=("Segoe UI", 12, "bold"),
            height=38,
            corner_radius=8,
        )
        cancel_btn.pack(side="left", expand=True, fill="x", padx=(8, 0))

        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (520 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (230 // 2)
        dialog.geometry(f"520x230+{x}+{y}")

        dialog.wait_window()
        return result["name"]

    def _on_mode_change(self, value=None):
        for w in self.content.winfo_children():
            w.pack_forget()
        if self.mode_var.get() == self.t("text_tab"):
            self.text_frame.pack(fill="both", expand=True)
        else:
            self.file_frame.pack(fill="both", expand=True)

    def _prompt_content_format(self) -> bool:
        """Запитує один раз при перемиканні на режим 'Лише вміст' (HEX або текст)."""
        ans = messagebox.askyesnocancel(
            "Формат вмісту .txt",
            "Оберіть формат вмісту для режиму 'Лише вміст (.txt)':\n\n"
            "Так — файл містить HEX-рядок (0-9, a-f) і шифрується/розшифровується як HEX.\n"
            "Ні — звичайний текст (UTF-8) буде перетворено у HEX перед шифруванням і після розшифрування.\n"
            "Скасувати — не перемикати режим.",
        )
        if ans is None:
            return False
        self.content_data_format = "hex" if ans else "text"
        return True

    def _on_file_process_mode_change(self, value=None):
        new_mode = self.file_process_mode.get()
        if new_mode == self._prev_file_process_mode:
            return
        if new_mode == "Лише вміст (.txt)":
            ok = self._prompt_content_format()
            if not ok:
                self.file_process_mode.set(self._prev_file_process_mode)
                return
        self._prev_file_process_mode = new_mode

    def _build_text_tab(self):
        f = self.text_frame

        prog_btn_frame = CTkFrame(f, fg_color=self.bg_color)
        prog_btn_frame.pack(fill="x", pady=(0, 8))

        def toggle_prog_info():
            if self.show_prog_info_text:
                self.prog_info_box_text.pack_forget()
                prog_info_btn.configure(text=self.t("about_program"))
                self.show_prog_info_text = False
            else:
                self.prog_info_box_text.pack(fill="x", pady=(0, 12), before=info_btn_frame)
                prog_info_btn.configure(text=self.t("about_program_expanded"))
                self.show_prog_info_text = True

        prog_info_btn = CTkButton(
            prog_btn_frame,
            text=self.t("about_program"),
            command=toggle_prog_info,
            fg_color="#FFB74D",
            hover_color="#FF9800",
            font=("Segoe UI", 12, "bold"),
            height=36,
        )
        prog_info_btn.pack(anchor="w")

        self.prog_info_box_text = CTkFrame(f, fg_color="#FFE8D6", corner_radius=8)

        prog_title = CTkLabel(
            self.prog_info_box_text,
            text=self.t("about_program_title"),
            font=("Segoe UI", 13, "bold"),
            text_color="#E65100",
        )
        prog_title.pack(anchor="w", padx=12, pady=(10, 4))

        prog_text = CTkLabel(
            self.prog_info_box_text,
            text=self.about_text_common,
            font=("Segoe UI", 12),
            text_color="#E65100",
            justify="left",
        )
        prog_text.pack(anchor="w", padx=12, pady=(0, 10))

        info_btn_frame = CTkFrame(f, fg_color=self.bg_color)
        info_btn_frame.pack(fill="x", pady=(0, 8))

        def toggle_text_info():
            self.show_text_info = not self.show_text_info
            if self.show_text_info:
                self.text_info_box.pack(fill="x", pady=(0, 12), before=self.text_input_frame)
                toggle_btn.configure(text=self.t("how_it_works_expanded"))
            else:
                self.text_info_box.pack_forget()
           

                toggle_btn.configure(text=self.t("how_it_works"))

        toggle_btn = CTkButton(
            info_btn_frame,
            text=self.t("how_it_works"),
            command=toggle_text_info,
            fg_color="#9E9E9E",
            hover_color="#757575",
            font=("Segoe UI", 12, "bold"),
            height=32,
        )
        toggle_btn.pack(anchor="w")

        pad_local_text = CTkFrame(info_btn_frame, fg_color=self.bg_color)
        pad_local_text.pack(fill="x", pady=(6, 0))
        CTkSegmentedButton(
            pad_local_text,
            values=["PKCS#7", "Немає"],
            variable=self.padding_mode_global,
            font=("Segoe UI", 11, "bold"),
        ).pack(side="left")
        pad_local_help_t = CTkLabel(pad_local_text, text="❓", font=("Segoe UI", 10))
        pad_local_help_t.pack(side="left", padx=6)
        create_tooltip(
            pad_local_help_t,
            "Перемикач доповнення (Текст):\n"
            " • PKCS#7 — авто-доповнення до 16 байт\n"
            " • Немає — без доповнення (кратно 16)."
        )

        

        self.text_info_box = CTkFrame(f, fg_color=self.info_color, corner_radius=8)

        info_title = CTkLabel(
            self.text_info_box,
            text=self.t("how_it_works_title"),
            font=("Segoe UI", 14, "bold"),
            text_color=self.text_color,
        )
        info_title.pack(anchor="w", padx=12, pady=(10, 4))

        info_text = CTkLabel(
            self.text_info_box,
            text=self.t("how_it_works_text"),
            font=("Segoe UI", 11, "bold"),
            text_color=self.text_color,
            justify="left",
        )
        info_text.pack(anchor="w", padx=12, pady=(0, 10))

        self.text_input_frame = CTkFrame(f, fg_color=self.bg_color)
        self.text_input_frame.pack(fill="both", expand=True)

        in_sec = CTkFrame(
            self.text_input_frame,
            fg_color="white",
            border_width=1,
            border_color="#D0D0D0",
            corner_radius=8,
        )
        in_sec.pack(fill="x", pady=(0, 10))

        in_header = CTkFrame(in_sec, fg_color="white")
        in_header.pack(fill="x", padx=12, pady=(10, 0))

        in_lbl = CTkLabel(in_header, text=self.t("input_text"), font=("Segoe UI", 15, "bold"))
        in_lbl.pack(side="left")

        q_mark = CTkLabel(in_header, text="❓", font=("Segoe UI", 10))
        q_mark.pack(side="left", padx=(6, 0))
        create_tooltip(q_mark, "Вводьте будь-який текст. Довжина не обмежена.")

        self.text_input_format = ctk.StringVar(value="text")
        text_fmt_top = CTkSegmentedButton(
            in_header,
            values=["text", "hex"],
            variable=self.text_input_format,
            font=("Segoe UI", 11, "bold"),
        )
        text_fmt_top.pack(side="right")

        fmt_frame = CTkFrame(in_sec, fg_color="white")
        fmt_frame.pack(fill="x", padx=12, pady=(4, 0))
        paste_btn = CTkButton(
            fmt_frame,
            text=self.t("paste"),
            command=self._paste_to_text,
            fg_color=self.paste_soft,
            hover_color=self.paste_soft_hover,
            height=30,
            width=100,
            font=("Segoe UI", 11, "bold"),
        )
        paste_btn.pack(side="right")
        create_tooltip(paste_btn, "Вставити текст із буфера обміну (Ctrl+V).")

        self.text_input = CTkTextbox(in_sec, height=130, font=("Segoe UI", 13))
        self.text_input.pack(fill="both", padx=12, pady=(6, 12))

        # --- Ключ ---
        key_sec = CTkFrame(
            self.text_input_frame,
            fg_color="white",
            border_width=1,
            border_color="#D0D0D0",
            corner_radius=8,
        )
        key_sec.pack(fill="x", pady=(0, 10))

        key_header = CTkFrame(key_sec, fg_color="white")
        key_header.pack(fill="x", padx=12, pady=(10, 0))

        key_lbl = CTkLabel(
            key_header, text=self.t("encryption_key"), font=("Segoe UI", 15, "bold")
        )
        key_lbl.pack(side="left")

        key_q = CTkLabel(key_header, text="❓", font=("Segoe UI", 10))
        key_q.pack(side="left", padx=(6, 0))
        create_tooltip(
            key_q,
            "Ключ має містити рівно 32 HEX-символи (0–9, a–f).\n"
            "Приклад: 0123456789abcdef0123456789abcdef.\n"
            "Натисніть «Згенерувати» для випадкового ключа.",
        )

        self.key_input_format = ctk.StringVar(value="hex")
        key_fmt_top = CTkSegmentedButton(
            key_header,
            values=["text", "hex"],
            variable=self.key_input_format,
            font=("Segoe UI", 11, "bold"),
        )
        key_fmt_top.pack(side="right")

        key_fmt_frame = CTkFrame(key_sec, fg_color="white")
        key_fmt_frame.pack(fill="x", padx=12, pady=(4, 0))
        paste_key_btn = CTkButton(
            key_fmt_frame,
            text=self.t("paste_key"),
            command=self._paste_to_key,
            fg_color=self.paste_soft,
            hover_color=self.paste_soft_hover,
            height=30,
            width=130,
            font=("Segoe UI", 11, "bold"),
        )
        paste_key_btn.pack(side="right")
        create_tooltip(paste_key_btn, "Вставити ключ із буфера обміну (Ctrl+V).")

        self.text_key = CTkEntry(
            key_sec,
            placeholder_text=self.t("key_placeholder"),
            font=("Courier New", 13, "bold"),
        )
        self.text_key.pack(fill="x", padx=12, pady=(6, 12))

        self.text_input.bind("<Control-v>", self._paste_to_text)
        self.text_input.bind("<Control-V>", self._paste_to_text)
        self.text_input.bind("<Button-3>", self._show_text_context_menu)

        self.text_key.bind("<Control-v>", self._paste_to_key)
        self.text_key.bind("<Control-V>", self._paste_to_key)
        self.text_key.bind("<Button-3>", self._show_key_context_menu)

        btn_frame = CTkFrame(self.text_input_frame, fg_color=self.bg_color)
        btn_frame.pack(fill="x", pady=(0, 10))

        gen_btn = CTkButton(
            btn_frame,
            text=self.t("generate_key"),
            command=self._gen_key_text,
            fg_color=self.secondary_soft,
            hover_color=self.secondary_soft_hover,
            font=("Segoe UI", 12, "bold"),
            height=40,
        )
        gen_btn.pack(side="left", padx=4, fill="x", expand=True)
        create_tooltip(gen_btn, "Створити випадковий 128-бітний ключ.")

        enc_btn = CTkButton(
            btn_frame,
            text=self.t("encrypt"),
            command=self._encrypt_text,
            fg_color=self.accent_color,
            hover_color="#005A9E",
            font=("Segoe UI", 12, "bold"),
            height=40,
        )
        enc_btn.pack(side="left", padx=4, fill="x", expand=True)
        create_tooltip(enc_btn, "Зашифрувати текст за алгоритмом SM4 (ECB).")

        dec_btn = CTkButton(
            btn_frame,
            text=self.t("decrypt"),
            command=self._decrypt_text,
            fg_color=self.success_color,
            hover_color="#1F8449",
            font=("Segoe UI", 12, "bold"),
            height=40,
        )
        dec_btn.pack(side="left", padx=4, fill="x", expand=True)
        create_tooltip(dec_btn, "Розшифрувати HEX-шифртекст у початковий текст.")

        out_sec = CTkFrame(
            self.text_input_frame,
            fg_color="white",
            border_width=1,
            border_color="#D0D0D0",
            corner_radius=8,
        )
        out_sec.pack(fill="both", expand=True)

        out_header = CTkFrame(out_sec, fg_color="white")
        out_header.pack(fill="x", padx=12, pady=(10, 0))

        out_lbl = CTkLabel(
            out_header,
            text=self.t("result"),
            font=("Segoe UI", 15, "bold"),
        )
        out_lbl.pack(side="left")

        out_q = CTkLabel(out_header, text="❓", font=("Segoe UI", 10))
        out_q.pack(side="left", padx=(6, 0))
        create_tooltip(
            out_q,
            "У цьому полі показується результат операції.\n"
            "• Після шифрування — шифртекст у HEX.\n"
            "• Після розшифрування — відновлений текст.",
        )

        out_actions = CTkFrame(out_header, fg_color="white")
        out_actions.pack(side="right")

        copy_btn = CTkButton(
            out_actions,
            text="📋 Копіювати",
            command=self._copy_text_output,
            fg_color=self.paste_soft,
            hover_color=self.paste_soft_hover,
            height=28,
            width=120,
            font=("Segoe UI", 11, "bold"),
        )
        copy_btn.pack(side="right")

        copy_info = CTkLabel(
            out_header,
            text="(Ctrl+A – виділити все, Ctrl+C – скопіювати)",
            font=("Segoe UI", 10, "bold"),
            text_color="#999999",
        )
        copy_info.pack(side="right", padx=(0, 10))

        self.text_output = CTkTextbox(out_sec, height=160, font=("Courier New", 13))
        self.text_output.pack(fill="both", padx=12, pady=(6, 12))
        self.text_output.configure(state="disabled")

    def _paste_to_text(self, event=None):
        """Вставка з буфера обміну у поле вхідного тексту."""
        try:
            txt = self.clipboard_get()
        except tk.TclError:
            messagebox.showwarning(
                "Буфер обміну порожній",
                "Спочатку скопіюйте текст (Ctrl+C), а потім спробуйте вставити ще раз.",
            )
            return "break"
        if not txt:
            messagebox.showwarning(
                "Буфер обміну порожній",
                "Буфер обміну не містить тексту.",
            )
            return "break"
        self.text_input.insert("insert", txt)
        return "break"

    def _paste_to_key(self, event=None):
        """Вставка з буфера обміну у поле ключа."""
        try:
            txt = self.clipboard_get()
        except tk.TclError:
            messagebox.showwarning(
                "Буфер обміну порожній",
                "Скопіюйте ключ (Ctrl+C), а потім вставте його (Ctrl+V) у поле.",
            )
            return "break"
        if not txt:
            messagebox.showwarning(
                "Буфер обміну порожній",
                "Буфер обміну не містить тексту ключа.",
            )
            return "break"
        # замінюємо вміст поля ключа вставленим текстом
        self.text_key.delete(0, tk.END)
        self.text_key.insert(0, txt.strip())
        return "break"

    def _copy_text_output(self):
        """Копіює вміст поля результату у буфер обміну."""
        content = self.text_output.get("1.0", "end").strip()
        if not content:
            messagebox.showwarning(
                "Немає даних",
                "Поле результату порожнє — копіювати нічого.",
            )
            return
        self.clipboard_clear()
        self.clipboard_append(content)
        self.update_idletasks()

    def _show_text_context_menu(self, event=None):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Вставити", command=self._paste_to_text)
        menu.add_command(
            label="Копіювати",
            command=lambda: self.text_input.event_generate("<<Copy>>"),
        )
        menu.add_command(
            label="Вирізати",
            command=lambda: self.text_input.event_generate("<<Cut>>"),
        )
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def _show_key_context_menu(self, event=None):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Вставити", command=self._paste_to_key)
        menu.add_command(
            label="Копіювати",
            command=lambda: self.text_key.event_generate("<<Copy>>"),
        )
        menu.add_command(
            label="Вирізати",
            command=lambda: self.text_key.event_generate("<<Cut>>"),
        )
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def _gen_key_text(self):
        try:
            k = generate_key()
            self.text_key.delete(0, "end")
            self.text_key.insert(0, k.hex())
            messagebox.showinfo(
                "Ключ згенеровано",
                "Новий випадковий 128-бітний ключ успішно згенеровано\n"
                "та вставлено у поле ключа.",
            )
        except Exception as e:
            messagebox.showerror(
                "Помилка генерації ключа",
                f"Під час генерації ключа сталася помилка:\n{e}",
            )

    def _encrypt_text(self):
        txt = self.text_input.get("1.0", "end").strip()
        if not txt:
            messagebox.showwarning(
                "Немає даних",
                "Введіть або вставте текст, який потрібно зашифрувати.",
            )
            return

        k = self.text_key.get().strip()
        if not k:
            messagebox.showwarning(
                "Ключ не задано",
                "Введіть ключ (32 HEX-символи) або натисніть «Згенерувати новий ключ».",
            )
            return

        if self.key_input_format.get() == "hex":
            try:
                key = bytes.fromhex(k)
            except ValueError:
                messagebox.showerror(
                    "Некоректний формат ключа",
                    "Ключ містить недопустимі символи.\n"
                    "Дозволені тільки цифри 0–9 та літери a–f (A–F), без пробілів.",
                )
                return
        else:
            # Ключ як довільний текст → UTF-8 байти
            key = k.encode("utf-8")

        if len(key) != 16:
            messagebox.showerror(
                "Некоректна довжина ключа",
                f"Отримано {len(key)} байтів ключа.\n"
                "Для SM4 потрібен ключ рівно 16 байтів (32 HEX-символи або 16 байтів тексту).",
            )
            return

        try:
            # Текст згідно формату
            if self.text_input_format.get() == "hex":
                try:
                    data = bytes.fromhex(txt)
                except ValueError:
                    messagebox.showerror(
                        "Некоректний HEX-текст",
                        "Поле «Вхідний текст» містить не HEX-символи."
                    )
                    return
            else:
                data = txt.encode("utf-8")

            if self.padding_mode_global.get() == "PKCS#7":
                ct = sm4_encrypt_ecb(data, key)
            else:
                if len(data) % 16 != 0:
                    messagebox.showerror(
                        "Некоректна довжина",
                        "Для режиму без доповнення довжина даних повинна бути кратною 16 байтам."
                    )
                    return
                # Блочне шифрування
                cipher = SM4(key)
                out = bytearray()
                for i in range(0, len(data), 16):
                    out.extend(cipher.encrypt_block(data[i:i+16]))
                ct = bytes(out)
            self.text_output.configure(state="normal")
            self.text_output.delete("1.0", "end")
            self.text_output.insert("1.0", ct.hex())
            self.text_output.configure(state="disabled")
            messagebox.showinfo(
                "Шифрування виконано",
                f"Текст успішно зашифровано.\n"
                f"Довжина шифртексту у HEX: {len(ct.hex())} символів.",
            )
        except Exception as e:
            messagebox.showerror(
                "Помилка шифрування",
                f"Під час шифрування сталася помилка:\n{e}",
            )

    def _decrypt_text(self):
        hex_in = self.text_input.get("1.0", "end").strip()
        if not hex_in:
            messagebox.showwarning(
                "Немає даних",
                "Вставте або введіть HEX-шифртекст, який потрібно розшифрувати.",
            )
            return

        k = self.text_key.get().strip()
        if not k:
            messagebox.showwarning(
                "Ключ не задано",
                "Введіть ключ (32 HEX-символи), який використовувався при шифруванні.",
            )
            return

        if self.key_input_format.get() == "hex":
            try:
                key = bytes.fromhex(k)
            except ValueError:
                messagebox.showerror(
                    "Некоректний формат ключа",
                    "Ключ містить недопустимі символи.\n"
                    "Перевірте, що у ключі тільки 0–9 та a–f, без пробілів.",
                )
                return
        else:
            key = k.encode("utf-8")

        if len(key) != 16:
            messagebox.showerror(
                "Некоректна довжина ключа",
                f"Отримано {len(key)} байтів ключа.\n"
                "Для SM4 потрібен ключ рівно 16 байтів (32 HEX-символи або 16 байтів тексту).",
            )
            return

        try:
            ct = bytes.fromhex(hex_in)
        except ValueError:
            messagebox.showerror(
                "Некоректний HEX-шифртекст",
                "Поле «Вхідний текст» має містити тільки HEX-символи (0–9, a–f), без пробілів.\n"
                "Скопіюйте шифртекст з поля результату шифрування без змін.",
            )
            return

        try:
            if self.padding_mode_global.get() == "PKCS#7":
                pt = sm4_decrypt_ecb(ct, key)
            else:
                if len(ct) % 16 != 0:
                    messagebox.showerror(
                        "Некоректна довжина",
                        "Для режиму без доповнення довжина шифртексту повинна бути кратною 16 байтам."
                    )
                    return
                cipher = SM4(key)
                out = bytearray()
                for i in range(0, len(ct), 16):
                    out.extend(cipher.decrypt_block(ct[i:i+16]))
                pt = bytes(out)

            self.text_output.configure(state="normal")
            self.text_output.delete("1.0", "end")
            pretty_hex = format_hex_block(pt)
            self.text_output.insert("1.0", pretty_hex)
            self.text_output.configure(state="disabled")
            messagebox.showinfo(
                "Розшифрування виконано",
                "Шифртекст успішно розшифровано. Результат показано у HEX.",
            )
        except Exception as e:
            messagebox.showerror(
                "Помилка розшифрування",
                "Не вдалося розшифрувати текст.\n\n"
                "Можливі причини:\n"
                " • використано неправильний ключ;\n"
                " • шифртекст пошкоджений або обрізаний;\n"
                " • дані були зашифровані іншим алгоритмом чи режимом.\n\n"
                f"Технічна інформація:\n{e}",
            )


    def _build_file_tab(self):
        f = self.file_frame

        prog_btn_frame = CTkFrame(f, fg_color=self.bg_color)
        prog_btn_frame.pack(fill="x", pady=(0, 8))

        def toggle_prog_info():
            if self.show_prog_info_file:
                self.prog_info_box_file.pack_forget()
                prog_info_btn.configure(text=self.t("about_program"))
                self.show_prog_info_file = False
            else:
                self.prog_info_box_file.pack(fill="x", pady=(0, 12), before=info_btn_frame)
                prog_info_btn.configure(text=self.t("about_program_expanded"))
                self.show_prog_info_file = True

        prog_info_btn = CTkButton(
            prog_btn_frame,
            text=self.t("about_program"),
            command=toggle_prog_info,
            fg_color="#FFB74D",
            hover_color="#FF9800",
            font=("Segoe UI", 12, "bold"),
            height=36,
        )
        prog_info_btn.pack(anchor="w")

        self.prog_info_box_file = CTkFrame(f, fg_color="#FFE8D6", corner_radius=8)

        prog_title = CTkLabel(
            self.prog_info_box_file,
            text=self.t("about_program_title"),
            font=("Segoe UI", 13, "bold"),
            text_color="#E65100",
        )
        prog_title.pack(anchor="w", padx=12, pady=(10, 4))

        prog_text = CTkLabel(
            self.prog_info_box_file,
            text=self.about_text_common,
            font=("Segoe UI", 12),
            text_color="#E65100",
            justify="left",
        )
        prog_text.pack(anchor="w", padx=12, pady=(0, 10))

        info_btn_frame = CTkFrame(f, fg_color=self.bg_color)
        info_btn_frame.pack(fill="x", pady=(0, 8))

        def toggle_file_info():
            self.show_file_info = not self.show_file_info
            if self.show_file_info:
                self.file_info_box.pack(fill="x", pady=(0, 12), before=self.file_content_frame)
                toggle_btn.configure(text=self.t("how_it_works_expanded"))
            else:
                self.file_info_box.pack_forget()
                toggle_btn.configure(text=self.t("how_it_works"))

        toggle_btn = CTkButton(
            info_btn_frame,
            text=self.t("how_it_works"),
            command=toggle_file_info,
            fg_color="#9E9E9E",
            hover_color="#757575",
            font=("Segoe UI", 12, "bold"),
            height=32,
        )
        toggle_btn.pack(anchor="w")

        pad_local_files = CTkFrame(info_btn_frame, fg_color=self.bg_color)
        pad_local_files.pack(fill="x", pady=(6, 0))
        CTkSegmentedButton(
            pad_local_files,
            values=["PKCS#7", "Немає"],
            variable=self.padding_mode_global,
            font=("Segoe UI", 11, "bold"),
        ).pack(side="left")
        pad_local_help_f = CTkLabel(pad_local_files, text="❓", font=("Segoe UI", 10))
        pad_local_help_f.pack(side="left", padx=6)
        create_tooltip(
            pad_local_help_f,
            "Перемикач доповнення (Файли):\n"
            " • PKCS#7 — авто-доповнення до 16 байт\n"
            " • Немає — без доповнення (кратно 16)"
        )

        mode_row = CTkFrame(pad_local_files, fg_color=self.bg_color)
        mode_row.pack(side="right")
        mode_lbl = CTkLabel(mode_row, text=self.t("mode_label"), font=("Segoe UI", 11, "bold"))
        mode_lbl.pack(side="left", padx=(0, 6))
        mode_q = CTkLabel(mode_row, text="❓", font=("Segoe UI", 10))
        mode_q.pack(side="left", padx=(0, 6))
        create_tooltip(
            mode_q,
            "Файл цілком — шифрування будь-якого типу файлів.\n"
            "Лише вміст (.txt) — читає текстовий файл, переводить текст у HEX перед шифруванням; ключові файли також повинні бути .txt."
        )
        CTkSegmentedButton(
            mode_row,
            values=[self.t("whole_file"), self.t("content_only")],
            variable=self.file_process_mode,
            command=self._on_file_process_mode_change,
            font=("Segoe UI", 11, "bold"),
        ).pack(side="left")

        self.file_info_box = CTkFrame(f, fg_color=self.info_color, corner_radius=8)

        info_title = CTkLabel(
            self.file_info_box,
            text=self.t("how_it_works_files_title"),
            font=("Segoe UI", 14, "bold"),
            text_color=self.text_color,
        )
        info_title.pack(anchor="w", padx=12, pady=(10, 4))

        info_text = CTkLabel(
            self.file_info_box,
            text=self.t("how_it_works_files"),
            font=("Segoe UI", 11, "bold"),
            text_color=self.text_color,
            justify="left",
        )
        info_text.pack(anchor="w", padx=12, pady=(0, 10))

        self.file_content_frame = CTkFrame(f, fg_color=self.bg_color)
        self.file_content_frame.pack(fill="both", expand=True)

        file_frame = CTkFrame(
            self.file_content_frame,
            fg_color="white",
            border_width=1,
            border_color="#D0D0D0",
            corner_radius=8,
        )
        file_frame.pack(fill="x", pady=(0, 10))

        file_header = CTkFrame(file_frame, fg_color="white")
        file_header.pack(fill="x", padx=12, pady=(10, 0))

        file_lbl = CTkLabel(
            file_header, text=self.t("file_selection"), font=("Segoe UI", 15, "bold")
        )
        file_lbl.pack(side="left")

        file_q = CTkLabel(file_header, text="❓", font=("Segoe UI", 10))
        file_q.pack(side="left", padx=(6, 0))
        create_tooltip(file_q, "Виберіть файл, який потрібно зашифрувати або розшифрувати.")

        self.file_label = CTkLabel(
            file_frame,
            text=self.t("no_file_selected"),
            text_color="#888888",
            font=("Segoe UI", 13, "bold"),
        )
        self.file_label.pack(side="left", padx=12, pady=10, fill="x", expand=True)

        browse_btn = CTkButton(
            file_frame,
            text=self.t("select_file"),
            command=self._browse_file,
            fg_color=self.accent_color,
            hover_color="#005A9E",
            font=("Segoe UI", 11, "bold"),
            height=40,
        )
        browse_btn.pack(side="right", padx=12, pady=10)
        create_tooltip(browse_btn, "Відкрити діалог вибору файлу.")

        key_frame = CTkFrame(
            self.file_content_frame,
            fg_color="white",
            border_width=1,
            border_color="#D0D0D0",
            corner_radius=8,
        )
        key_frame.pack(fill="x", pady=(0, 10))

        key_header = CTkFrame(key_frame, fg_color="white")
        key_header.pack(fill="x", padx=12, pady=(10, 0))

        key_lbl = CTkLabel(
            key_header, text=self.t("key_management"), font=("Segoe UI", 15, "bold")
        )
        key_lbl.pack(side="left")

        key_q = CTkLabel(key_header, text="❓", font=("Segoe UI", 10))
        key_q.pack(side="left", padx=(6, 0))
        create_tooltip(
            key_q,
            "Згенеруйте новий ключ або завантажте існуючий з файлу (32 HEX-символи).",
        )

        key_btn_frame = CTkFrame(key_frame, fg_color="white")
        key_btn_frame.pack(fill="x", padx=12, pady=(6, 0))

        gen_btn = CTkButton(
            key_btn_frame,
            text=self.t("generate_key_btn"),
            command=self._gen_key,
            fg_color=self.secondary_soft,
            hover_color=self.secondary_soft_hover,
            font=("Segoe UI", 11, "bold"),
            height=40,
        )
        gen_btn.pack(side="left", padx=4, fill="x", expand=True)
        create_tooltip(gen_btn, "Створити новий випадковий 128-бітний ключ.")

        load_btn = CTkButton(
            key_btn_frame,
            text=self.t("load_key_btn"),
            command=self._load_key,
            fg_color="#9C27B0",
            hover_color="#7B1FA2",
            font=("Segoe UI", 11, "bold"),
            height=40,
        )
        load_btn.pack(side="left", padx=4, fill="x", expand=True)
        create_tooltip(load_btn, "Завантажити ключ з текстового файлу в HEX-форматі.")

        key_label_frame = CTkFrame(key_frame, fg_color="white")
        key_label_frame.pack(fill="x", padx=12, pady=(6, 12))

        self.key_label = CTkLabel(
            key_label_frame,
            text="🔑 Ключ не обрано",
            text_color="#888888",
            font=("Segoe UI", 12, "bold"),
        )
        self.key_label.pack(side="left", fill="x", expand=True)

        # Кнопки дій
        action_frame = CTkFrame(self.file_content_frame, fg_color=self.bg_color)
        action_frame.pack(fill="both", expand=True)

        enc_btn = CTkButton(
            action_frame,
            text=self.t("encrypt_file"),
            command=self._encrypt_file,
            fg_color=self.accent_color,
            hover_color="#005A9E",
            font=("Segoe UI", 12, "bold"),
            height=48,
        )
        enc_btn.pack(fill="x", pady=(0, 8))
        create_tooltip(enc_btn, "Зашифрувати обраний файл з використанням поточного ключа.")

        dec_btn = CTkButton(
            action_frame,
            text=self.t("decrypt_file"),
            command=self._decrypt_file,
            fg_color=self.success_color,
            hover_color="#1F8449",
            font=("Segoe UI", 12, "bold"),
            height=48,
        )
        dec_btn.pack(fill="x")
        create_tooltip(dec_btn, "Розшифрувати раніше зашифрований файл (.txt).")

    def _browse_file(self):
        content_mode = self.is_content_mode()
        filetypes = [("Усі файли", "*.*")] if not content_mode else [("Текстові файли", "*.txt"), ("Усі файли", "*.*")]
        p = filedialog.askopenfilename(
            title="Виберіть файл для шифрування / розшифрування",
            filetypes=filetypes,
        )
        if not p:
            return
        candidate = Path(p)
        if content_mode and candidate.suffix.lower() != ".txt":
            messagebox.showerror(
                "Неправильний формат",
                "У режимі 'Лише вміст (.txt)' можна обрати лише текстові файли (.txt).",
            )
            return
        self.enc_file = candidate
        self.file_label.configure(text=f"📎 {self.enc_file.name}")
        messagebox.showinfo(
            "Файл обрано",
            f"Файл для обробки:\n{self.enc_file.name}",
        )
        
    def _choose_output_path_encrypt(self) -> Path | None:
        """Запитує користувача: автоматично зберегти поруч або створити новий файл.
        Повертає шлях збереження або None якщо скасовано."""
        if not self.enc_file:
            messagebox.showwarning(
                "Файл не вибрано",
                "Спочатку оберіть файл для шифрування",
            )
            return None
        content_mode = self.is_content_mode()
        if content_mode and self.enc_file.suffix.lower() != ".txt":
            messagebox.showerror(
                "Неправильний формат",
                "У режимі 'Лише вміст (.txt)' можна шифрувати лише .txt файли.",
            )
            return None
        ans = messagebox.askyesnocancel(
            "Збереження файлу",
            "Створити новий файл у вибраному місці?\n\n"
            "Так — задати назву та місце.\n"
            "Ні — зберегти поруч із джерелом автоматично.",
        )
        if ans is None:
            return None
        auto_name = f"{self.enc_file.stem}_encrypted"
        if content_mode:
            auto_name += ".txt"
        if ans is False:
            return self.enc_file.with_name(auto_name)
        default_name = auto_name
        name = self._prompt_name_modal(
            "Назва файлу",
            "Вкажіть назву зашифрованого файлу (без розширення):",
            default_name,
        )
        if not name:
            return None
        dir_ = filedialog.askdirectory(
            title="Оберіть папку для збереження зашифрованого файлу",
        )
        if not dir_:
            return None
        out_path = Path(dir_) / name
        if content_mode and out_path.suffix.lower() != ".txt":
            out_path = out_path.with_name(out_path.name + ".txt")
        return out_path

    def _choose_output_path_decrypt(self, source_path: Path) -> Path | None:
        """Аналогічний вибір для розшифрування."""
        file_path = source_path
        # Автоматичне ім'я за замовчуванням
        content_mode = self.is_content_mode()
        if content_mode and file_path.suffix.lower() != ".txt":
            messagebox.showerror(
                "Неправильний формат",
                "У режимі 'Лише вміст (.txt)' можна розшифровувати лише файли .txt.",
            )
            return None
        if file_path.stem.endswith("_encrypted"):
            base_name = file_path.stem[:-10]
        else:
            base_name = file_path.stem + "_decrypted"
        if content_mode:
            auto_name = base_name + ".txt"
        else:
            auto_name = base_name + file_path.suffix
        auto_out = file_path.with_name(auto_name)

        ans = messagebox.askyesnocancel(
            "Збереження файлу",
            "Створити новий файл у вибраному місці?\n\n"
            "Так — задати назву та місце.\n"
            "Ні — зберегти поруч із джерелом автоматично.",
        )
        if ans is None:
            return None
        if ans is False:
            return auto_out
        name = self._prompt_name_modal(
            "Назва файлу",
            "Вкажіть назву розшифрованого файлу:",
            auto_out.name,
        )
        if not name:
            return None
        dir_ = filedialog.askdirectory(
            title="Оберіть папку для збереження розшифрованого файлу",
        )
        if not dir_:
            return None
        out_path = Path(dir_) / name
        if content_mode and out_path.suffix.lower() != ".txt":
            out_path = out_path.with_name(out_path.name + ".txt")
        return out_path

    def _gen_key(self):
        try:
            k = generate_key()
            self.enc_key = k
            self.key_label.configure(text=f"🔑 {k.hex()}")
            messagebox.showinfo(
                "Ключ згенеровано",
                "Новий випадковий 128-бітний ключ успішно згенеровано.",
            )
        except Exception as e:
            messagebox.showerror(
                "Помилка генерації ключа",
                f"Під час генерації ключа сталася помилка:\n{e}",
            )

    def _load_key(self):
        content_mode = self.is_content_mode()
        key_filetypes = [("Усі файли", "*.*")] if not content_mode else [("Текстові файли", "*.txt"), ("Усі файли", "*.*")]
        p = filedialog.askopenfilename(
            title="Виберіть файл ключа (HEX або бінарний)",
            filetypes=key_filetypes,
        )
        if not p:
            return
        if content_mode and Path(p).suffix.lower() != ".txt":
            messagebox.showerror(
                "Неправильний файл ключа",
                "У режимі 'Лише вміст (.txt)' ключовий файл має бути у форматі .txt.",
            )
            return
        try:
            k = load_key(p)
        except Exception as e:
            messagebox.showerror(
                "Помилка завантаження ключа",
                f"Не вдалося завантажити ключ з файлу:\n{e}",
            )
            return
        self.enc_key = k
        self.key_label.configure(text=f"🔑 {k.hex()}")
        messagebox.showinfo(
            "Ключ завантажено",
            f"Ключ успішно завантажено з файлу:\n{Path(p).name}",
        )

    def _encrypt_file(self):
        if not self.enc_file:
            messagebox.showwarning(
                "Файл не вибрано",
                "Спочатку оберіть файл, який потрібно зашифрувати.",
            )
            return
        if not self.enc_key:
            messagebox.showwarning(
                "Ключ не задано",
                "Згенеруйте новий ключ або завантажте його з файлу\n"
                "перед шифруванням.",
            )
            return
        content_mode = self.is_content_mode()
        try:
            if content_mode:
                if self.enc_file.suffix.lower() != ".txt":
                    messagebox.showerror(
                        "Неправильний формат",
                        "У режимі 'Лише вміст (.txt)' можна шифрувати лише текстові файли (.txt).",
                    )
                    return
                try:
                    text_data = self.enc_file.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    messagebox.showerror(
                        "Помилка читання",
                        "Не вдалося прочитати файл як UTF-8. Перевірте кодування тексту.",
                    )
                    return
                if self.content_data_format == "hex":
                    try:
                        data = parse_hex_string(text_data)
                    except ValueError as exc:
                        messagebox.showerror("Некоректний HEX", str(exc))
                        return
                    ct_encode = lambda b: format_hex_block(b)
                else:
                    data = text_data.encode("utf-8")
                    # Мапимо байти шифртексту у текст через latin-1, щоб зберегти у UTF-8-файлі
                    ct_encode = lambda b: b.decode("latin-1")
            else:
                data = self.enc_file.read_bytes()
                ct_encode = None
            if self.padding_mode_global.get() == "PKCS#7":
                ct = sm4_encrypt_ecb(data, self.enc_key)
            else:
                if len(data) % 16 != 0:
                    messagebox.showerror(
                        "Некоректна довжина",
                        "Без доповнення довжина файлу повинна бути кратною 16 байтам."
                    )
                    return
                cipher = SM4(self.enc_key)
                out = bytearray()
                for i in range(0, len(data), 16):
                    out.extend(cipher.encrypt_block(data[i:i+16]))
                ct = bytes(out)
            # Запитати користувача про спосіб збереження
            out = self._choose_output_path_encrypt()
            if out is None:
                return
            if content_mode:
                out.write_text(ct_encode(ct), encoding="utf-8")
            else:
                out.write_bytes(ct)
            messagebox.showinfo(
                "Шифрування файлу виконано",
                f"Файл успішно зашифровано.\n\nРезультат збережено як:\n{out.name}",
            )
        except Exception as e:
            messagebox.showerror(
                "Помилка шифрування файлу",
                f"Під час шифрування файлу сталася помилка:\n{e}",
            )

    def _decrypt_file(self):
        # Використовуємо вже обраний файл, якщо він є
        content_mode = self.is_content_mode()
        filetypes = [("Усі файли", "*.*")] if not content_mode else [("Текстові файли", "*.txt"), ("Усі файли", "*.*")]
        if self.enc_file is not None and self.enc_file.exists():
            p = str(self.enc_file)
        else:
            # Якщо файл не обрано раніше, запропонувати вибір
            p = filedialog.askopenfilename(
                title="Виберіть зашифрований файл",
                filetypes=filetypes,
            )
            if not p:
                return

        file_path = Path(p)
        if content_mode and file_path.suffix.lower() != ".txt":
            messagebox.showerror(
                "Неправильний формат",
                "У режимі 'Лише вміст (.txt)' можна розшифровувати лише файли .txt.",
            )
            return

        if not self.enc_key:
            k_file = filedialog.askopenfilename(
                title="Ключ не задано. Виберіть файл ключа (HEX або бінарний)",
                filetypes=[("Текстові файли", "*.txt"), ("Усі файли", "*.*")] if content_mode else [("Усі файли", "*.*")],
            )
            if not k_file:
                messagebox.showwarning(
                    "Ключ не задано",
                    "Без ключа неможливо розшифрувати файл.\n"
                    "Повторіть спробу та вкажіть файл ключа.",
                )
                return
            if content_mode and Path(k_file).suffix.lower() != ".txt":
                messagebox.showerror(
                    "Неправильний файл ключа",
                    "У режимі 'Лише вміст (.txt)' ключовий файл має бути у форматі .txt.",
                )
                return
            try:
                key = load_key(k_file)
            except Exception as e:
                messagebox.showerror(
                    "Помилка завантаження ключа",
                    f"Не вдалося завантажити ключ з файлу:\n{e}",
                )
                return
        else:
            key = self.enc_key

        try:
            ct_raw = file_path.read_text(encoding="utf-8") if content_mode else file_path.read_bytes()
            if content_mode:
                if self.content_data_format == "hex":
                    try:
                        ct = parse_hex_string(ct_raw)
                    except ValueError as exc:
                        messagebox.showerror("Некоректний HEX", str(exc))
                        return
                else:
                    # Шифртекст збережено як текст, кожен байт через latin-1, файл у UTF-8
                    ct = ct_raw.encode("latin-1")
            else:
                ct = ct_raw
            if self.padding_mode_global.get() == "PKCS#7":
                pt_bytes = sm4_decrypt_ecb(ct, key)
            else:
                if len(ct) % 16 != 0:
                    messagebox.showerror(
                        "Некоректна довжина",
                        "Без доповнення довжина шифртексту повинна бути кратною 16 байтам."
                    )
                    return
                cipher = SM4(key)
                outb = bytearray()
                for i in range(0, len(ct), 16):
                    outb.extend(cipher.decrypt_block(ct[i:i+16]))
                pt_bytes = bytes(outb)
            if content_mode:
                if self.content_data_format == "hex":
                    output_text = format_hex_block(pt_bytes)
                else:
                    try:
                        output_text = pt_bytes.decode("utf-8")
                    except UnicodeDecodeError:
                        output_text = pt_bytes.decode("utf-8", errors="replace")
            # Запитати користувача про спосіб збереження
            out = self._choose_output_path_decrypt(file_path)
            if out is None:
                return
            if content_mode:
                out.write_text(output_text, encoding="utf-8")
            else:
                out.write_bytes(pt_bytes)
            extra = " (HEX-рядок)" if content_mode and self.content_data_format == "hex" else (" (UTF-8)" if content_mode else "")
            messagebox.showinfo(
                "Розшифрування файлу виконано",
                f"Файл успішно розшифровано{extra}.\n\nРезультат збережено як:\n{out.name}",
            )
        except Exception as e:
            messagebox.showerror(
                "Помилка розшифрування файлу",
                "Не вдалося розшифрувати файл.\n\n"
                "Можливі причини:\n"
                " • використано неправильний ключ;\n"
                " • файл було змінено або пошкоджено;\n"
                " • файл не був зашифрований цією програмою.\n\n"
                f"Технічна інформація:\n{e}",
            )


if __name__ == "__main__":
    app = SM4App()
    app.mainloop()



