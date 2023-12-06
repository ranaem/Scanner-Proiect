#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 13:16:44 2023

@author: ranaemad
"""

import re

# Token types
class TokenType:
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    OPERATOR = "OPERATOR"
    NUMERIC = "NUMERIC"
    STRING_LITERAL = "STRING_LITERAL"
    CHARACTER_LITERAL = "CHARACTER_LITERAL"
    SEMICOLON = "SEMICOLON"
    OPEN_PAREN = "OPEN_PAREN"
    CLOSE_PAREN = "CLOSE_PAREN"
    OPEN_BRACE = "OPEN_BRACE"
    CLOSE_BRACE = "CLOSE_BRACE"
    COMMA = "COMMA"
    END_OF_INPUT = "END_OF_INPUT"
    WHITESPACE = "WHITESPACE"

# Token class
class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

# Lexical Analyzer
def lex_c_code_from_file(file_path):
    with open(file_path, 'r') as file:
        c_code = file.read()
    return lex_c_code(c_code)

def lex_c_code(input_code):
    tokens = []
    patterns = [
        (r"\b(int|char|void|return|auto|break|case|const|continue|default|enum|float|double|bool|extern|unsigned|goto|static|class|struct|for|if|else|register|long|while|do|short|signed|sizeof|switch|typedef|union|volatile)\b", TokenType.KEYWORD),
        (r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", TokenType.IDENTIFIER),
        (r"\b[0-9]+\b", TokenType.NUMERIC),
        (r'\"(?:\\.|[^\\"])*\"', TokenType.STRING_LITERAL),
        (r"\'(?:\\.|[^\\'])\'", TokenType.CHARACTER_LITERAL),
        (r"\+|\-|\*|\/|\%|\=|<|>", TokenType.OPERATOR),
        (r";", TokenType.SEMICOLON),
        (r"\(", TokenType.OPEN_PAREN),
        (r"\)", TokenType.CLOSE_PAREN),
        (r"\{", TokenType.OPEN_BRACE),
        (r"\}", TokenType.CLOSE_BRACE),
        (r",", TokenType.COMMA),
        (r" ", TokenType().WHITESPACE)
    ]

    # Remove comments and white spaces
    input_code = re.sub(r'\/\/[^\n]*', '', input_code)  # Remove // comments
    input_code = re.sub(r'\/\*.*?\*\/', '', input_code, flags=re.DOTALL)  # Remove /* */ comments
    input_code = re.sub(r'\s+', ' ', input_code)  # Replace multiple spaces with a single space
    input_code = input_code.strip()

    while input_code:
        match = None
        for pattern, token_type in patterns:
            regex = re.compile(pattern)
            match = regex.match(input_code)
            if match:
                value = match.group(0)
                if token_type != TokenType.WHITESPACE:
                    tokens.append(Token(token_type, value))
                input_code = input_code[len(value):]
                break

        if not match or not input_code.strip():
            break

    tokens.append(Token(TokenType.END_OF_INPUT))
    return tokens

# Write tokens to a file
def write_tokens_to_file(tokens, output_file_path):
    with open(output_file_path, 'w') as output_file:
        for token in tokens:
            if token.type == TokenType.END_OF_INPUT:
                output_file.write("End of input\n")
            else:
                output_file.write(f"Type: {token.type}, Value: {token.value}\n")

# Test the lexical analyzer with code from a file
input_file_path = "/Users/ranaemad/Downloads/lexical.txt"
output_file_path = "/Users/ranaemad/Downloads/output.txt"

tokens = lex_c_code_from_file(input_file_path)
write_tokens_to_file(tokens, output_file_path)