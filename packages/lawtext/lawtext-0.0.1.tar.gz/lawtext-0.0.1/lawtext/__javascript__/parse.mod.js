	__nest__ (
		__all__,
		'lawtext.parse', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var re = {};
					__nest__ (re, '', __init__ (__world__.re));
					var DEFAULT_INDENT = '\u3000';
					var LawtextParseError = __class__ ('LawtextParseError', [Exception], {
						get __init__ () {return __get__ (this, function (self, message, lineno, lines) {
							__super__ (LawtextParseError, '__init__') (self, message);
							self.message = message;
							self.lineno = lineno;
							self.lines = lines;
						}, '__init__');},
						get __str__ () {return __get__ (this, function (self) {
							var lines = function () {
								var __accu0__ = [];
								for (var lineno = max (0, self.lineno - 2); lineno < min (len (self.lines), (self.lineno + 2) + 1); lineno++) {
									__accu0__.append ('{}{}|{}\n'.format ((lineno == self.lineno ? '==>' : '   '), lineno, self.lines [lineno]));
								}
								return __accu0__;
							} ();
							var lines_str = ''.join (lines);
							return (self.message + '\n\n') + lines_str;
						}, '__str__');}
					});
					var LexerError = __class__ ('LexerError', [Exception], {
						get __init__ () {return __get__ (this, function (self, message, lineno) {
							__super__ (LexerError, '__init__') (self, message);
							self.message = message;
							self.lineno = lineno;
						}, '__init__');}
					});
					var LexerInternalError = __class__ ('LexerInternalError', [Exception], {
						get __init__ () {return __get__ (this, function (self, message) {
							__super__ (LexerInternalError, '__init__') (self, message);
							self.message = message;
						}, '__init__');}
					});
					var ParserError = __class__ ('ParserError', [Exception], {
						get __init__ () {return __get__ (this, function (self, message, lineno) {
							__super__ (ParserError, '__init__') (self, message);
							self.message = message;
							self.lineno = lineno;
						}, '__init__');}
					});
					var re_DETECT_INDENT = re.compile ('^(?P<indent>[ \\t\\f\\v]+)\\S.*$');
					var detect_indent = function (lines) {
						var indents = set ();
						var __iterable0__ = lines;
						for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
							var line = __iterable0__ [__index0__];
							var match = re_DETECT_INDENT.match (line);
							if (match) {
								indents.add (match.group (1));
							}
						}
						if (!(len (indents))) {
							return DEFAULT_INDENT;
						}
						var indents = sorted (indents, __kwargtrans__ ({key: len}));
						return indents [0];
					};
					var indent_level = function (indents, indent) {
						var __left0__ = re.subn (indent, '', indents);
						var s = __left0__ [0];
						var n = __left0__ [1];
						if (s) {
							var indent_description = indent;
							var indent_description = re.sub (' ', '<半角スペース>', indent_description);
							var indent_description = re.sub ('\u3000', '<全角スペース>', indent_description);
							var indent_description = re.sub ('\t', '<tab>', indent_description);
							var __except0__ = LexerInternalError ('インデントの文字が整っていません。なお、この文書で用いられているインデント文字は、「{}」＝「{}」であると推測されました。'.format (indent, indent_description));
							__except0__.__cause__ = null;
							throw __except0__;
						}
						return n;
					};
					var re_TC1stLine = re.compile ('^(?P<indents>\\s*)\\* - (?P<tcbody>.*)$');
					var re_TCnthLine = re.compile ('^(?P<indents>\\s*)  - (?P<tcbody>.*)$');
					var re_FigLine = re.compile ('^(?P<indents>\\s*)\\.\\.(?:\\s+)figure::(?:\\s+)(?P<figbody>.*)$');
					var re_DefaultLine = re.compile ('^(?P<indents>\\s*)(?P<linebody>\\S.*)$');
					var re_BlankLine = re.compile ('^\\s*$');
					var lex_line = function (line, indent) {
						var match = re_TC1stLine.match (line);
						if (match) {
							return list (['TC1stLine', indent_level (match.group (1), indent), lex_tcbody (match.group (2))]);
						}
						var match = re_TCnthLine.match (line);
						if (match) {
							return list (['TCnthLine', indent_level (match.group (1), indent), lex_tcbody (match.group (2))]);
						}
						var match = re_FigLine.match (line);
						if (match) {
							return list (['FigLine', indent_level (match.group (1), indent), dict ({'body': match.group (2)})]);
						}
						var match = re_DefaultLine.match (line);
						if (match) {
							return list (['DefaultLine', indent_level (match.group (1), indent), dict ({'body': match.group (2)})]);
						}
						var match = re_BlankLine.match (line);
						if (match) {
							return list (['BlankLine', 0, dict ({'body': ''})]);
						}
						var __except0__ = LexerInternalError ('行の構造が判別できません。');
						__except0__.__cause__ = null;
						throw __except0__;
					};
					var re_Arg = re.compile ('^\\[(?P<name>\\S+?)="?(?P<value>\\S+?)"?\\]');
					var lex_tcbody = function (tcbody) {
						var attr = dict ({});
						var body = tcbody;
						while (true) {
							var match = re_Arg.match (body);
							if (!(match)) {
								break;
							}
							attr [match.group (1)] = match.group (2);
							var body = re_Arg.sub ('', body, __kwargtrans__ ({count: 1}));
						}
						return dict ({'attr': attr, 'body': body});
					};
					var lex = function (lines) {
						var indent = detect_indent (lines);
						var ret = list ([]);
						var __iterable0__ = enumerate (lines);
						for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
							var __left0__ = __iterable0__ [__index0__];
							var lineno = __left0__ [0];
							var line = __left0__ [1];
							try {
								ret.append (lex_line (line, indent));
							}
							catch (__except0__) {
								if (isinstance (__except0__, LexerInternalError)) {
									var error = __except0__;
									var __except1__ = LexerError (error.message, lineno);
									__except1__.__cause__ = null;
									throw __except1__;
								}
								else {
									throw __except0__;
								}
							}
						}
						return ret;
					};
					var PARENTHESIS_PAIRS = list ([tuple ([re.compile ('[(（]'), re.compile ('[)）]')]), tuple ([re.compile ('「'), re.compile ('」')])]);
					var re_FORCE_EXIT_PARENTHESIS = re.compile ('」');
					var SENTENCE_DELIMITERS = list ([re.compile ('。')]);
					var skip_parenthesis = function (text, pos) {
						var __left0__ = tuple ([null, null]);
						var re_sp = __left0__ [0];
						var re_ep = __left0__ [1];
						var __iterable0__ = PARENTHESIS_PAIRS;
						for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
							var re_pair = __iterable0__ [__index0__];
							if (re_pair [0].match (text [pos])) {
								var __left0__ = re_pair;
								var re_sp = __left0__ [0];
								var re_ep = __left0__ [1];
								break;
							}
						}
						if (re_sp && re_ep) {
							pos++;
							while (pos < len (text)) {
								var old_pos = pos;
								var pos = skip_parenthesis (text, pos);
								if (pos != old_pos) {
									continue;
								}
								if (re_ep.match (text [pos])) {
									pos++;
									break;
								}
								if (re_FORCE_EXIT_PARENTHESIS.match (text [pos])) {
									break;
								}
								pos++;
							}
						}
						return pos;
					};
					var split_sentences = function (text) {
						var sentences = list ([]);
						var start_pos = 0;
						var pos = 0;
						while (pos < len (text)) {
							var old_pos = pos;
							var pos = skip_parenthesis (text, pos);
							if (pos != old_pos) {
								continue;
							}
							var __iterable0__ = SENTENCE_DELIMITERS;
							for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
								var sentence_delimiter = __iterable0__ [__index0__];
								if (sentence_delimiter.match (text [pos])) {
									pos++;
									sentences.append (text.__getslice__ (start_pos, pos, 1));
									var start_pos = pos;
									continue;
								}
							}
							pos++;
						}
						if (start_pos < len (text)) {
							sentences.append (text.__getslice__ (start_pos, null, 1));
						}
						return sentences;
					};
					var py_split = function (text) {
						var split_text = list ([]);
						var start_pos = 0;
						var pos = 0;
						while (pos < len (text)) {
							var old_pos = pos;
							var pos = skip_parenthesis (text, pos);
							if (pos != old_pos) {
								continue;
							}
							if (!(text [pos].strip ())) {
								split_text.append (text.__getslice__ (start_pos, pos, 1));
								pos++;
								var start_pos = pos;
							}
							pos++;
						}
						if (start_pos < len (text)) {
							split_text.append (text.__getslice__ (start_pos, null, 1));
						}
						return split_text;
					};
					var get_sentences = function (text) {
						var els = list ([]);
						var text_split = py_split (text);
						if (len (text_split) >= 2) {
							var __iterable0__ = text_split;
							for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
								var column = __iterable0__ [__index0__];
								els.append (dict ({'tag': 'Column', 'attr': dict ({}), 'children': function () {
									var __accu0__ = [];
									var __iterable1__ = split_sentences (column);
									for (var __index1__ = 0; __index1__ < __iterable1__.length; __index1__++) {
										var sentence = __iterable1__ [__index1__];
										__accu0__.append (dict ({'tag': 'Sentence', 'attr': dict ({}), 'children': list ([sentence])}));
									}
									return __accu0__;
								} ()}));
							}
						}
						else {
							els.extend (function () {
								var __accu0__ = [];
								var __iterable0__ = split_sentences (text);
								for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
									var sentence = __iterable0__ [__index0__];
									__accu0__.append (dict ({'tag': 'Sentence', 'attr': dict ({}), 'children': list ([sentence])}));
								}
								return __accu0__;
							} ());
						}
						return els;
					};
					var re_LawNum = re.compile ('^[(（](?P<body>.+?)[）)](?:\\s*)$');
					var re_ArticleRange = re.compile ('(?P<body>[(（].+?[）)])(?:\\s*)$');
					var re_ArticleCaption = re.compile ('^[(（](?P<body>.+?)[）)](?:\\s*)$');
					var re_ArticleBody = re.compile ('^(?P<title>\\S+)\\s+(?P<body>\\S.*)(?:\\s*)$');
					var re_ParagraphCaption = re.compile ('^[(（](?P<body>.+?)[）)](?:\\s*)$');
					var re_ParagraphItemBody = re.compile ('^(?P<title>\\S+)\\s+(?P<body>\\S.*)(?:\\s*)$');
					var re_SupplProvisionLabel = re.compile ('^(?P<title>.+?)\\s*(?:[(（](?P<amend_law_num>.+?)[）)])?(?:\\s+(?P<extract>抄?))?(?:\\s*)$');
					var re_AppdxTableLabel = re.compile ('^(?P<title>.+?)\\s*(?:(?P<related_article_num>[(（].+?[）)]))?(?:\\s*)$');
					var re_AppdxStyleLabel = re.compile ('^(?P<title>.+?)\\s*(?:(?P<related_article_num>[(（].+?[）)]))?(?:\\s*)$');
					var Parser = __class__ ('Parser', [object], {
						get __init__ () {return __get__ (this, function (self, lexed_lines, lineno) {
							if (typeof lineno == 'undefined' || (lineno != null && lineno .hasOwnProperty ("__kwargtrans__"))) {;
								var lineno = 0;
							};
							self.lexed_lines = lexed_lines;
							self.lineno = lineno;
						}, '__init__');},
						get py_get () {return __get__ (this, function (self, lineno) {
							if ((0 <= lineno && lineno < len (self.lexed_lines))) {
								return self.lexed_lines [lineno];
							}
							else {
								return tuple (['BlankLine', 0, dict ({})]);
							}
						}, 'get');},
						get continuing () {return __get__ (this, function (self) {
							return self.lineno < len (self.lexed_lines);
						}, 'continuing');},
						get forward () {return __get__ (this, function (self) {
							self.lineno++;
						}, 'forward');},
						get here () {return __get__ (this, function (self) {
							return self.py_get (self.lineno);
						}, 'here');},
						get prev () {return __get__ (this, function (self) {
							return self.py_get (self.lineno - 1);
						}, 'prev');},
						get py_next () {return __get__ (this, function (self) {
							return self.py_get (self.lineno + 1);
						}, 'next');},
						get skip_blank_lines () {return __get__ (this, function (self) {
							while (self.continuing ()) {
								var __left0__ = self.here ();
								var line_type = __left0__ [0];
								var indent = __left0__ [1];
								var data = __left0__ [2];
								if (line_type == 'BlankLine') {
									self.forward ();
								}
								else {
									break;
								}
							}
						}, 'skip_blank_lines');},
						get process_title () {return __get__ (this, function (self) {
							self.skip_blank_lines ();
							var law_title = null;
							var law_num = null;
							var __left0__ = self.here ();
							var line_type = __left0__ [0];
							var indent = __left0__ [1];
							var data = __left0__ [2];
							var __left0__ = self.py_next ();
							var next_line_type = __left0__ [0];
							var next_indent = __left0__ [1];
							var next_data = __left0__ [2];
							var body_split = py_split (data ['body']);
							if (line_type == 'DefaultLine' && indent == 0 && len (body_split) == 1 && (next_line_type == 'BlankLine' || next_line_type == 'DefaultLine' && next_indent == 0)) {
								var law_title = dict ({'tag': 'LawTitle', 'attr': dict ({}), 'children': list ([data ['body']])});
								self.forward ();
								if (self.continuing ()) {
									var __left0__ = self.here ();
									var line_type = __left0__ [0];
									var indent = __left0__ [1];
									var data = __left0__ [2];
									if (line_type == 'DefaultLine') {
										var match = re_LawNum.match (data ['body']);
										if (!(match)) {
											ParserError ('法令番号は括弧（\u3000）で囲ってください。', lineno);
										}
										var law_num = dict ({'tag': 'LawNum', 'attr': dict ({}), 'children': list ([match.group (1)])});
										self.forward ();
									}
								}
							}
							return tuple ([law_title, law_num]);
						}, 'process_title');},
						get process_enact_statement () {return __get__ (this, function (self) {
							self.skip_blank_lines ();
							var enact_statement = null;
							var __left0__ = self.here ();
							var line_type = __left0__ [0];
							var indent = __left0__ [1];
							var data = __left0__ [2];
							var __left0__ = self.py_next ();
							var next_line_type = __left0__ [0];
							var next_indent = __left0__ [1];
							var next_data = __left0__ [2];
							var body_split = py_split (data ['body']);
							if (indent == 0 && len (body_split) == 1 && next_line_type == 'BlankLine') {
								var enact_statement = dict ({'tag': 'EnactStatement', 'attr': dict ({}), 'children': list ([data ['body']])});
								self.forward ();
							}
							return enact_statement;
						}, 'process_enact_statement');},
						get process_toc_group () {return __get__ (this, function (self) {
							self.skip_blank_lines ();
							var toc_group = null;
							var __left0__ = self.here ();
							var line_type = __left0__ [0];
							var indent = __left0__ [1];
							var data = __left0__ [2];
							var __left0__ = self.py_next ();
							var next_line_type = __left0__ [0];
							var next_indent = __left0__ [1];
							var next_data = __left0__ [2];
							var body_split = re.py_split ('\\s+', re.py_split ('の', data ['body']) [0]);
							if (line_type == 'DefaultLine') {
								var toc_group_children = list ([]);
								var toc_group_char = body_split [0] [len (body_split [0]) - 1];
								var title = re_ArticleRange.sub ('', data ['body']);
								var title_tag = dict ({'編': 'PartTitle', '章': 'ChapterTitle', '節': 'SectionTitle', '款': 'SubsectionTitle', '目': 'DivisionTitle', '条': 'ArticleTitle', '則': 'SupplProvisionLabel'}) [toc_group_char];
								toc_group_children.append (dict ({'tag': title_tag, 'attr': dict ({}), 'children': list ([title])}));
								var match = re_ArticleRange.search (data ['body']);
								if (match) {
									toc_group_children.append (dict ({'tag': 'ArticleRange', 'attr': dict ({}), 'children': list ([match.group (1)])}));
								}
								self.forward ();
								var toc_base_indent = indent;
								while (self.continuing ()) {
									var __left0__ = self.here ();
									var line_type = __left0__ [0];
									var indent = __left0__ [1];
									var data = __left0__ [2];
									if (line_type == 'DefaultLine') {
										if (indent <= toc_base_indent) {
											break;
										}
										else if (indent != toc_base_indent + 1) {
											ParserError ('目次の内容のインデントが整っていません。', lineno);
										}
										var sub_toc_group = self.process_toc_group ();
										if (sub_toc_group) {
											toc_group_children.append (sub_toc_group);
										}
										else {
											break;
										}
									}
									else {
										break;
									}
								}
								var toc_tag = dict ({'編': 'TOCPart', '章': 'TOCChapter', '節': 'TOCSection', '款': 'TOCSubsection', '目': 'TOCDivision', '条': 'TOCArticle', '則': 'TOCSupplProvision'}) [toc_group_char];
								var toc_group = dict ({'tag': toc_tag, 'attr': dict ({}), 'children': toc_group_children});
							}
							return toc_group;
						}, 'process_toc_group');},
						get process_toc () {return __get__ (this, function (self) {
							self.skip_blank_lines ();
							var toc = null;
							var __left0__ = self.here ();
							var line_type = __left0__ [0];
							var indent = __left0__ [1];
							var data = __left0__ [2];
							var __left0__ = self.py_next ();
							var next_line_type = __left0__ [0];
							var next_indent = __left0__ [1];
							var next_data = __left0__ [2];
							var body_split = py_split (data ['body']);
							if (indent == 0 && len (body_split) == 1 && next_line_type == 'DefaultLine') {
								var toc_children = list ([]);
								toc_children.append (dict ({'tag': 'TOCLabel', 'attr': dict ({}), 'children': list ([data ['body']])}));
								self.forward ();
								var toc_base_indent = indent;
								while (self.continuing ()) {
									var __left0__ = self.here ();
									var line_type = __left0__ [0];
									var indent = __left0__ [1];
									var data = __left0__ [2];
									if (line_type == 'DefaultLine') {
										if (indent != toc_base_indent + 1) {
											ParserError ('目次の内容のインデントが整っていません。', lineno);
										}
										var toc_group = self.process_toc_group ();
										if (toc_group) {
											toc_children.append (toc_group);
										}
										else {
											break;
										}
									}
									else {
										break;
									}
								}
								var toc = dict ({'tag': 'TOC', 'attr': dict ({}), 'children': toc_children});
							}
							return toc;
						}, 'process_toc');},
						get process_main_provision () {return __get__ (this, function (self) {
							self.skip_blank_lines ();
							var main_provision = null;
							var main_provision_children = list ([]);
							while (self.continuing ()) {
								var article_group = self.process_article_group ();
								if (article_group) {
									main_provision_children.append (article_group);
								}
								else {
									var articles = self.process_articles ();
									if (len (articles)) {
										main_provision_children.extend (articles);
									}
									else {
										break;
									}
								}
							}
							if (len (main_provision_children)) {
								var main_provision = dict ({'tag': 'MainProvision', 'attr': dict ({}), 'children': main_provision_children});
							}
							return main_provision;
						}, 'process_main_provision');},
						get process_article_group () {return __get__ (this, function (self, parent_group_tag) {
							if (typeof parent_group_tag == 'undefined' || (parent_group_tag != null && parent_group_tag .hasOwnProperty ("__kwargtrans__"))) {;
								var parent_group_tag = '';
							};
							self.skip_blank_lines ();
							var article_group = null;
							var __left0__ = self.here ();
							var line_type = __left0__ [0];
							var indent = __left0__ [1];
							var data = __left0__ [2];
							var __left0__ = self.py_next ();
							var next_line_type = __left0__ [0];
							var next_indent = __left0__ [1];
							var next_data = __left0__ [2];
							var body_split = re.py_split ('\\s+', re.py_split ('の', data ['body']) [0]);
							var article_group_char = body_split [0] [len (body_split [0]) - 1];
							var article_group_tag_rank = dict ({'': 0, 'Part': 1, 'Chapter': 2, 'Section': 3, 'Subsection': 4, 'Division': 5});
							var article_group_tags = dict ({'編': 'Part', '章': 'Chapter', '節': 'Section', '款': 'Subsection', '目': 'Division'});
							if (indent != 0 && __in__ (article_group_char, article_group_tags) && article_group_tag_rank [article_group_tags [article_group_char]] > article_group_tag_rank [parent_group_tag] && next_line_type == 'BlankLine') {
								var article_group_tag = article_group_tags [article_group_char];
								var article_group_title_tag = dict ({'編': 'PartTitle', '章': 'ChapterTitle', '節': 'SectionTitle', '款': 'SubsectionTitle', '目': 'DivisionTitle', '条': 'ArticleTitle'}) [article_group_char];
								var article_group_children = list ([]);
								article_group_children.append (dict ({'tag': article_group_title_tag, 'attr': dict ({}), 'children': list ([data ['body']])}));
								self.forward ();
								self.skip_blank_lines ();
								while (self.continuing ()) {
									var __left0__ = self.here ();
									var line_type = __left0__ [0];
									var indent = __left0__ [1];
									var data = __left0__ [2];
									var sub_article_group = self.process_article_group (article_group_tag);
									if (sub_article_group) {
										article_group_children.append (sub_article_group);
									}
									else {
										var articles = self.process_articles ();
										if (len (articles)) {
											article_group_children.extend (articles);
										}
										else {
											break;
										}
									}
								}
								if (len (article_group_children)) {
									var article_group = dict ({'tag': article_group_tag, 'attr': dict ({}), 'children': article_group_children});
								}
							}
							return article_group;
						}, 'process_article_group');},
						get process_articles () {return __get__ (this, function (self) {
							self.skip_blank_lines ();
							var articles = list ([]);
							while (self.continuing ()) {
								var article = self.process_article ();
								if (article) {
									articles.append (article);
								}
								else {
									break;
								}
							}
							return articles;
						}, 'process_articles');},
						get process_article () {return __get__ (this, function (self) {
							self.skip_blank_lines ();
							var article = null;
							var article_children = list ([]);
							var __left0__ = self.here ();
							var line_type = __left0__ [0];
							var indent = __left0__ [1];
							var data = __left0__ [2];
							var body_split = (len (data) ? py_split (data ['body']) : '');
							var __left0__ = self.py_next ();
							var next_line_type = __left0__ [0];
							var next_indent = __left0__ [1];
							var next_data = __left0__ [2];
							var next_body_split = (len (next_data) ? py_split (next_data ['body']) : '');
							var __left0__ = self.py_get (self.lineno + 2);
							var next2_line_type = __left0__ [0];
							var next2_indent = __left0__ [1];
							var next2_data = __left0__ [2];
							if (line_type == 'DefaultLine' && indent == 1 && re_ArticleCaption.match (data ['body']) && next_line_type == 'DefaultLine' && next_indent == 0 && !((len (next2_data) ? next2_data ['body'].startswith ('別表') : false)) && (re_ArticleBody.match (next_data ['body']) || len (next_body_split) == 1 && next2_line_type == 'DefaultLine' && next2_indent == 0 && re_ParagraphItemBody.match (next2_data ['body']))) {
								article_children.append (dict ({'tag': 'ArticleCaption', 'attr': dict ({}), 'children': list ([data ['body']])}));
								self.forward ();
								var __left0__ = self.here ();
								var line_type = __left0__ [0];
								var indent = __left0__ [1];
								var data = __left0__ [2];
								var body_split = (len (data) ? py_split (data ['body']) : '');
								var __left0__ = self.py_next ();
								var next_line_type = __left0__ [0];
								var next_indent = __left0__ [1];
								var next_data = __left0__ [2];
							}
							var match = re_ArticleBody.match (data ['body']);
							if (line_type == 'DefaultLine' && indent == 0 && !(data ['body'].startswith ('別表')) && (match || len (body_split) == 1 && next_line_type == 'DefaultLine' && next_indent == 0 && re_ParagraphItemBody.match (next_data ['body']))) {
								if (match) {
									var __left0__ = tuple ([match.group (1), match.group (2)]);
									var article_title = __left0__ [0];
									var _ = __left0__ [1];
								}
								else {
									var article_title = data ['body'];
								}
								article_children.append (dict ({'tag': 'ArticleTitle', 'attr': dict ({}), 'children': list ([article_title])}));
								var first_paragraph_in_article = true;
								if (!(match)) {
									article_children.append (dict ({'tag': 'Paragraph', 'attr': dict ({}), 'children': list ([dict ({'tag': 'ParagraphNum', 'attr': dict ({}), 'children': list ([])}), dict ({'tag': 'ParagraphSentence', 'attr': dict ({}), 'children': list ([dict ({'tag': 'Sentence', 'attr': dict ({}), 'children': list ([])})])})])}));
									self.forward ();
									var first_paragraph_in_article = false;
								}
								var paragraph_items = self.process_paragraph_items (indent, first_paragraph_in_article);
								if (len (paragraph_items)) {
									article_children.extend (paragraph_items);
								}
								var article = dict ({'tag': 'Article', 'attr': dict ({}), 'children': article_children});
							}
							return article;
						}, 'process_article');},
						get process_paragraph_items () {return __get__ (this, function (self, current_indent, in_article) {
							if (typeof current_indent == 'undefined' || (current_indent != null && current_indent .hasOwnProperty ("__kwargtrans__"))) {;
								var current_indent = 0;
							};
							if (typeof in_article == 'undefined' || (in_article != null && in_article .hasOwnProperty ("__kwargtrans__"))) {;
								var in_article = false;
							};
							self.skip_blank_lines ();
							var paragraph_items = list ([]);
							var first_paragraph_in_article = in_article;
							while (self.continuing ()) {
								var paragraph_item = self.process_paragraph_item (current_indent, first_paragraph_in_article);
								if (paragraph_item) {
									paragraph_items.append (paragraph_item);
									var first_paragraph_in_article = false;
								}
								else {
									break;
								}
							}
							return paragraph_items;
						}, 'process_paragraph_items');},
						get process_paragraph_item () {return __get__ (this, function (self, current_indent, first_paragraph_in_article) {
							if (typeof first_paragraph_in_article == 'undefined' || (first_paragraph_in_article != null && first_paragraph_in_article .hasOwnProperty ("__kwargtrans__"))) {;
								var first_paragraph_in_article = false;
							};
							self.skip_blank_lines ();
							var paragraph_item = null;
							var paragraph_item_children = list ([]);
							var __left0__ = self.here ();
							var line_type = __left0__ [0];
							var indent = __left0__ [1];
							var data = __left0__ [2];
							var __left0__ = self.py_next ();
							var next_line_type = __left0__ [0];
							var next_indent = __left0__ [1];
							var next_data = __left0__ [2];
							var next_match = (len (next_data) ? re_ParagraphItemBody.match (next_data ['body']) : null);
							if (!(first_paragraph_in_article) && line_type == 'DefaultLine' && indent == current_indent + 1 && re_ParagraphCaption.match (data ['body']) && next_line_type == 'DefaultLine' && next_indent == current_indent && next_match && !__in__ ('条', next_match.group (1)) && !__in__ ('附', next_match.group (1)) && !__in__ ('付', next_match.group (1)) && !(next_match.group (1).startswith ('別表'))) {
								paragraph_item_children.append (dict ({'tag': 'ParagraphCaption', 'attr': dict ({}), 'children': list ([data ['body']])}));
								self.forward ();
								var __left0__ = self.here ();
								var line_type = __left0__ [0];
								var indent = __left0__ [1];
								var data = __left0__ [2];
								var __left0__ = self.py_next ();
								var next_line_type = __left0__ [0];
								var next_indent = __left0__ [1];
								var next_data = __left0__ [2];
							}
							var paragraph_item_tags = dict ({0: 'Paragraph', 1: 'Item', 2: 'Subitem1', 3: 'Subitem2', 4: 'Subitem3', 5: 'Subitem4', 6: 'Subitem5', 7: 'Subitem6', 8: 'Subitem7', 9: 'Subitem8', 10: 'Subitem9', 11: 'Subitem10'});
							var paragraph_item_title_tags = dict ({0: 'ParagraphNum', 1: 'ItemTitle', 2: 'Subitem1Title', 3: 'Subitem2Title', 4: 'Subitem3Title', 5: 'Subitem4Title', 6: 'Subitem5Title', 7: 'Subitem6Title', 8: 'Subitem7Title', 9: 'Subitem8Title', 10: 'Subitem9Title', 11: 'Subitem10Title'});
							var paragraph_item_sentence_tags = dict ({0: 'ParagraphSentence', 1: 'ItemSentence', 2: 'Subitem1Sentence', 3: 'Subitem2Sentence', 4: 'Subitem3Sentence', 5: 'Subitem4Sentence', 6: 'Subitem5Sentence', 7: 'Subitem6Sentence', 8: 'Subitem7Sentence', 9: 'Subitem8Sentence', 10: 'Subitem9Sentence', 11: 'Subitem10Sentence'});
							var match = re_ParagraphItemBody.match (data ['body']);
							if (line_type == 'DefaultLine' && indent == current_indent && (match && !__in__ ('附', match.group (1)) && !__in__ ('付', match.group (1)) && !__in__ ('備考', match.group (1)) && (first_paragraph_in_article || !__in__ ('条', match.group (1)) && !(match.group (1).startswith ('別表'))) || indent == 0 && len (py_split (data ['body'])) == 1 && !(data ['body'].startswith ('別表')))) {
								if (first_paragraph_in_article || !(match)) {
									paragraph_item_children.append (dict ({'tag': 'ParagraphNum', 'attr': dict ({}), 'children': list ([])}));
								}
								else {
									var paragraph_item_title = match.group (1);
									var paragraph_item_title_tag = paragraph_item_title_tags [current_indent];
									paragraph_item_children.append (dict ({'tag': paragraph_item_title_tag, 'attr': dict ({}), 'children': list ([paragraph_item_title])}));
								}
								var paragraph_item_sentence_children = get_sentences ((match ? match.group (2) : data ['body']));
								var paragraph_item_sentence_tag = paragraph_item_sentence_tags [current_indent];
								paragraph_item_children.append (dict ({'tag': paragraph_item_sentence_tag, 'attr': dict ({}), 'children': paragraph_item_sentence_children}));
								self.forward ();
								var paragraph_item_tag = paragraph_item_tags [current_indent];
								var sub_paragraph_items = self.process_paragraph_items (current_indent + 1);
								if (len (sub_paragraph_items)) {
									paragraph_item_children.extend (sub_paragraph_items);
								}
								var table_struct = self.process_table_struct (current_indent + 1);
								if (table_struct) {
									paragraph_item_children.append (table_struct);
								}
								var list_ = self.process_list (current_indent + 2);
								if (list_) {
									paragraph_item_children.append (list_);
								}
								var paragraph_item = dict ({'tag': paragraph_item_tag, 'attr': dict ({}), 'children': paragraph_item_children});
							}
							return paragraph_item;
						}, 'process_paragraph_item');},
						get process_table_struct () {return __get__ (this, function (self, current_indent) {
							self.skip_blank_lines ();
							var table_struct = null;
							var table_children = list ([]);
							var table_struct_children = list ([]);
							var remarks = self.process_remarks (current_indent);
							if (remarks) {
								table_struct_children.append (remarks);
							}
							var __left0__ = self.here ();
							var line_type = __left0__ [0];
							var indent = __left0__ [1];
							var data = __left0__ [2];
							var __left0__ = self.py_next ();
							var next_line_type = __left0__ [0];
							var next_indent = __left0__ [1];
							var next_data = __left0__ [2];
							if (line_type == 'TC1stLine' && indent == current_indent) {
								var table_rows = self.process_table_rows (current_indent);
								if (len (table_rows)) {
									table_children.extend (table_rows);
									var table = dict ({'tag': 'Table', 'attr': dict ({}), 'children': table_children});
									table_struct_children.append (table);
								}
							}
							if (len (table_struct_children)) {
								var table_struct = dict ({'tag': 'TableStruct', 'attr': dict ({}), 'children': table_struct_children});
							}
							return table_struct;
						}, 'process_table_struct');},
						get process_table_rows () {return __get__ (this, function (self, current_indent) {
							var table_rows = list ([]);
							while (self.continuing ()) {
								var table_row = self.process_table_row (current_indent);
								if (table_row) {
									table_rows.append (table_row);
								}
								else {
									break;
								}
							}
							return table_rows;
						}, 'process_table_rows');},
						get process_table_row () {return __get__ (this, function (self, current_indent) {
							self.skip_blank_lines ();
							var table_row = null;
							var table_row_children = list ([]);
							var __left0__ = self.here ();
							var line_type = __left0__ [0];
							var indent = __left0__ [1];
							var data = __left0__ [2];
							var __left0__ = self.py_next ();
							var next_line_type = __left0__ [0];
							var next_indent = __left0__ [1];
							var next_data = __left0__ [2];
							if (line_type == 'TC1stLine' && indent == current_indent) {
								var table_columns = self.process_table_columns (current_indent);
								if (len (table_columns)) {
									table_row_children.extend (table_columns);
									var table_row = dict ({'tag': 'TableRow', 'attr': dict ({}), 'children': table_row_children});
								}
							}
							return table_row;
						}, 'process_table_row');},
						get process_table_columns () {return __get__ (this, function (self, current_indent) {
							var table_columns = list ([]);
							var first_column_processed = false;
							while (self.continuing ()) {
								var __left0__ = self.here ();
								var line_type = __left0__ [0];
								var indent = __left0__ [1];
								var data = __left0__ [2];
								if (!(first_column_processed) && line_type == 'TC1stLine' || first_column_processed && line_type == 'TCnthLine') {
									var table_column = self.process_table_column (current_indent);
									if (table_column) {
										table_columns.append (table_column);
										if (!(first_column_processed)) {
											var first_column_processed = true;
										}
									}
									else {
										break;
									}
								}
								else {
									break;
								}
							}
							return table_columns;
						}, 'process_table_columns');},
						get process_table_column () {return __get__ (this, function (self, current_indent) {
							self.skip_blank_lines ();
							var table_column = null;
							var table_column_children = list ([]);
							var __left0__ = self.here ();
							var line_type = __left0__ [0];
							var indent = __left0__ [1];
							var data = __left0__ [2];
							var __left0__ = self.py_next ();
							var next_line_type = __left0__ [0];
							var next_indent = __left0__ [1];
							var next_data = __left0__ [2];
							if (__in__ (line_type, tuple (['TC1stLine', 'TCnthLine'])) && indent == current_indent) {
								table_column_children.append (dict ({'tag': 'Sentence', 'attr': dict ({}), 'children': list ([data ['body']])}));
								self.forward ();
								var table_column_attr = data.py_get ('attr', dict ({}));
								var table_column_base_indent = indent;
								while (self.continuing ()) {
									var __left0__ = self.here ();
									var line_type = __left0__ [0];
									var indent = __left0__ [1];
									var data = __left0__ [2];
									var __left0__ = self.py_next ();
									var next_line_type = __left0__ [0];
									var next_indent = __left0__ [1];
									var next_data = __left0__ [2];
									if (line_type == 'DefaultLine' && indent == current_indent + 2) {
										table_column_children.append (dict ({'tag': 'Sentence', 'attr': dict ({}), 'children': list ([data ['body']])}));
										self.forward ();
									}
									else {
										break;
									}
								}
								var table_column = dict ({'tag': 'TableColumn', 'attr': table_column_attr, 'children': table_column_children});
							}
							return table_column;
						}, 'process_table_column');},
						get process_fig () {return __get__ (this, function (self, current_indent) {
							self.skip_blank_lines ();
							var fig = null;
							var __left0__ = self.here ();
							var line_type = __left0__ [0];
							var indent = __left0__ [1];
							var data = __left0__ [2];
							if (line_type == 'FigLine' && indent == current_indent) {
								var fig = dict ({'tag': 'Fig', 'attr': dict ({'src': data ['body']}), 'children': list ([])});
								self.forward ();
							}
							return fig;
						}, 'process_fig');},
						get process_list () {return __get__ (this, function (self, current_indent) {
							self.skip_blank_lines ();
							var list_ = null;
							var list_children = list ([]);
							var __left0__ = self.here ();
							var line_type = __left0__ [0];
							var indent = __left0__ [1];
							var data = __left0__ [2];
							var __left0__ = self.py_next ();
							var next_line_type = __left0__ [0];
							var next_indent = __left0__ [1];
							var next_data = __left0__ [2];
							var body_split = (len (data) ? py_split (data ['body']) : list (['']));
							if (line_type == 'DefaultLine' && indent == current_indent && !__in__ (body_split [0] [len (body_split [0]) - 1], tuple (['編', '章', '節', '款', '目', '条', '附', '付', '則']))) {
								var list_ = dict ({'tag': 'List', 'attr': dict ({}), 'children': list ([dict ({'tag': 'ListSentence', 'attr': dict ({}), 'children': get_sentences (data ['body'])})])});
								self.forward ();
							}
							return list_;
						}, 'process_list');},
						get process_suppl_provision () {return __get__ (this, function (self) {
							self.skip_blank_lines ();
							var suppl_provision = null;
							var suppl_provision_children = list ([]);
							var __left0__ = self.here ();
							var line_type = __left0__ [0];
							var indent = __left0__ [1];
							var data = __left0__ [2];
							var __left0__ = self.py_next ();
							var next_line_type = __left0__ [0];
							var next_indent = __left0__ [1];
							var next_data = __left0__ [2];
							var match = re_SupplProvisionLabel.match (data ['body']);
							var titlejoin = (match ? re.sub ('\\s+', '', match.group (1)) : '');
							if (line_type == 'DefaultLine' && indent != 0 && match && (titlejoin.startswith ('付則') || titlejoin.startswith ('附則'))) {
								var suppl_provision_attr = dict ({});
								if (match.group (3)) {
									suppl_provision_attr ['Extract'] = 'true';
								}
								if (match.group (2)) {
									suppl_provision_attr ['AmendLawNum'] = match.group (2);
								}
								suppl_provision_children.append (dict ({'tag': 'SupplProvisionLabel', 'attr': dict ({}), 'children': list ([match.group (1)])}));
								self.forward ();
								var articles_or_paragraph_items_processed = false;
								while (self.continuing ()) {
									var paragraph_items = self.process_paragraph_items ();
									if (len (paragraph_items)) {
										suppl_provision_children.extend (paragraph_items);
										var articles_or_paragraph_items_processed = true;
									}
									else {
										var articles = self.process_articles ();
										if (len (articles)) {
											suppl_provision_children.extend (articles);
											var articles_or_paragraph_items_processed = true;
										}
										else {
											break;
										}
									}
								}
								var __left0__ = self.here ();
								var line_type = __left0__ [0];
								var indent = __left0__ [1];
								var data = __left0__ [2];
								if (!(articles_or_paragraph_items_processed) && line_type == 'DefaultLine' && indent == 0) {
									suppl_provision_children.append (dict ({'tag': 'Paragraph', 'attr': dict ({}), 'children': list ([dict ({'tag': 'ParagraphNum', 'attr': dict ({}), 'children': list ([])}), dict ({'tag': 'ParagraphSentence', 'attr': dict ({}), 'children': get_sentences (data ['body'])})])}));
									self.forward ();
								}
								if (len (suppl_provision_children)) {
									var suppl_provision = dict ({'tag': 'SupplProvision', 'attr': suppl_provision_attr, 'children': suppl_provision_children});
								}
							}
							return suppl_provision;
						}, 'process_suppl_provision');},
						get process_appdx_table () {return __get__ (this, function (self) {
							self.skip_blank_lines ();
							var appdx_table = null;
							var appdx_table_children = list ([]);
							var __left0__ = self.here ();
							var line_type = __left0__ [0];
							var indent = __left0__ [1];
							var data = __left0__ [2];
							var __left0__ = self.py_next ();
							var next_line_type = __left0__ [0];
							var next_indent = __left0__ [1];
							var next_data = __left0__ [2];
							var match = re_AppdxTableLabel.match (data ['body']);
							var titlejoin = (match ? re.sub ('\\s+', '', match.group (1)) : '');
							if (line_type == 'DefaultLine' && indent == 0 && match && titlejoin.startswith ('別表')) {
								appdx_table_children.append (dict ({'tag': 'AppdxTableTitle', 'attr': dict ({}), 'children': list ([match.group (1)])}));
								if (match.group (2)) {
									appdx_table_children.append (dict ({'tag': 'RelatedArticleNum', 'attr': dict ({}), 'children': list ([match.group (2)])}));
								}
								self.forward ();
								var current_indent = indent;
								var paragraph_items = self.process_paragraph_items (current_indent + 1);
								if (len (paragraph_items)) {
									appdx_table_children.extend (paragraph_items);
								}
								var table_struct = self.process_table_struct (current_indent + 1);
								if (table_struct) {
									appdx_table_children.append (table_struct);
								}
								var appdx_table = dict ({'tag': 'AppdxTable', 'attr': dict ({}), 'children': appdx_table_children});
							}
							return appdx_table;
						}, 'process_appdx_table');},
						get process_appdx_style () {return __get__ (this, function (self) {
							self.skip_blank_lines ();
							var appdx_style = null;
							var appdx_style_children = list ([]);
							var style_struct_children = list ([]);
							var __left0__ = self.here ();
							var line_type = __left0__ [0];
							var indent = __left0__ [1];
							var data = __left0__ [2];
							var match = re_AppdxStyleLabel.match (data ['body']);
							var body_split = (len (data) ? re.py_split ('\\s+', data ['body'], __kwargtrans__ ({maxsplit: 1})) : list (['']));
							if (line_type == 'DefaultLine' && indent == 0 && body_split [0].startswith ('様式')) {
								appdx_style_children.append (dict ({'tag': 'AppdxStyleTitle', 'attr': dict ({}), 'children': list ([match.group (1)])}));
								if (match.group (2)) {
									appdx_style_children.append (dict ({'tag': 'RelatedArticleNum', 'attr': dict ({}), 'children': list ([match.group (2)])}));
								}
								self.forward ();
								var current_indent = indent;
								var remarks = self.process_remarks (current_indent + 1);
								if (remarks) {
									style_struct_children.append (remarks);
								}
								var fig = self.process_fig (current_indent + 1);
								if (fig) {
									var style = dict ({'tag': 'Style', 'attr': dict ({}), 'children': list ([fig])});
									style_struct_children.append (style);
								}
								var remarks = self.process_remarks (current_indent + 1);
								if (remarks) {
									style_struct_children.append (remarks);
								}
								if (len (style_struct_children)) {
									appdx_style_children.append (dict ({'tag': 'StyleStruct', 'attr': dict ({}), 'children': style_struct_children}));
								}
								var appdx_style = dict ({'tag': 'AppdxStyle', 'attr': dict ({}), 'children': appdx_style_children});
							}
							return appdx_style;
						}, 'process_appdx_style');},
						get process_remarks () {return __get__ (this, function (self, current_indent) {
							self.skip_blank_lines ();
							var remarks = null;
							var remarks_children = list ([]);
							var __left0__ = self.here ();
							var line_type = __left0__ [0];
							var indent = __left0__ [1];
							var data = __left0__ [2];
							var body_split = (len (data) ? re.py_split ('\\s+', data ['body'], __kwargtrans__ ({maxsplit: 1})) : list (['']));
							if (line_type == 'DefaultLine' && indent == current_indent && body_split [0].startswith ('備考')) {
								remarks_children.append (dict ({'tag': 'RemarksLabel', 'attr': dict ({}), 'children': list ([body_split [0]])}));
								if (len (body_split) > 1) {
									remarks_children.extend (get_sentences (body_split [1]));
								}
								self.forward ();
								var paragraph_items = self.process_paragraph_items (current_indent + 1);
								if (len (paragraph_items)) {
									remarks_children.extend (paragraph_items);
								}
								var remarks = dict ({'tag': 'Remarks', 'attr': dict ({}), 'children': remarks_children});
							}
							return remarks;
						}, 'process_remarks');},
						get process_law () {return __get__ (this, function (self) {
							self.skip_blank_lines ();
							var law_children = list ([]);
							var law_body_children = list ([]);
							var law_num = null;
							var __left0__ = self.process_title ();
							var law_title = __left0__ [0];
							var law_num = __left0__ [1];
							if (law_num) {
								law_children.append (law_num);
							}
							if (law_title) {
								law_body_children.append (law_title);
							}
							while (self.continuing ()) {
								var enact_statement = self.process_enact_statement ();
								if (enact_statement) {
									law_body_children.append (enact_statement);
									continue;
								}
								break;
							}
							var toc = self.process_toc ();
							if (toc) {
								law_body_children.append (toc);
							}
							var main_provision = self.process_main_provision ();
							if (main_provision) {
								law_body_children.append (main_provision);
							}
							while (self.continuing ()) {
								var suppl_provision = self.process_suppl_provision ();
								if (suppl_provision) {
									law_body_children.append (suppl_provision);
									continue;
								}
								var appdx_table = self.process_appdx_table ();
								if (appdx_table) {
									law_body_children.append (appdx_table);
									continue;
								}
								var appdx_style = self.process_appdx_style ();
								if (appdx_style) {
									law_body_children.append (appdx_style);
									continue;
								}
								break;
							}
							law_children.append (dict ({'tag': 'LawBody', 'attr': dict ({}), 'children': law_body_children}));
							return dict ({'tag': 'Law', 'attr': dict ({}), 'children': law_children});
						}, 'process_law');}
					});
					var parse_lawtext = function (lawtext) {
						var lines = re.py_split ('\\r\\n', lawtext);
						if (len (lines) <= 1) {
							var lines = re.py_split ('\\n', lawtext);
						}
						try {
							var lexed_lines = lex (lines);
						}
						catch (__except0__) {
							if (isinstance (__except0__, LexerError)) {
								var error = __except0__;
								var lineno = error.lineno;
								var __except1__ = LawtextParseError (error.message, lineno, lines);
								__except1__.__cause__ = null;
								throw __except1__;
							}
							else {
								throw __except0__;
							}
						}
						var parser = Parser (lexed_lines);
						try {
							var law = parser.process_law ();
						}
						catch (__except0__) {
							if (isinstance (__except0__, ParserError)) {
								var error = __except0__;
								var lineno = error.lineno;
								var __except1__ = LawtextParseError (error.message, lineno, lines);
								__except1__.__cause__ = null;
								throw __except1__;
							}
							else if (isinstance (__except0__, LawtextParseError)) {
								var e = __except0__;
								var __except1__ = e;
								__except1__.__cause__ = null;
								throw __except1__;
							}
							else if (isinstance (__except0__, Exception)) {
								var e = __except0__;
								var __except1__ = LawtextParseError ('この行の処理中にエラーが発生しました。', parser.lineno, lines);
								__except1__.__cause__ = null;
								throw __except1__;
							}
							else {
								throw __except0__;
							}
						}
						if (parser.continuing ()) {
							var lineno = parser.lineno;
							var __except0__ = LawtextParseError ('この行の種類が判別できません。', lineno, lines);
							__except0__.__cause__ = null;
							throw __except0__;
						}
						return law;
					};
					__pragma__ ('<use>' +
						're' +
					'</use>')
					__pragma__ ('<all>')
						__all__.DEFAULT_INDENT = DEFAULT_INDENT;
						__all__.LawtextParseError = LawtextParseError;
						__all__.LexerError = LexerError;
						__all__.LexerInternalError = LexerInternalError;
						__all__.PARENTHESIS_PAIRS = PARENTHESIS_PAIRS;
						__all__.Parser = Parser;
						__all__.ParserError = ParserError;
						__all__.SENTENCE_DELIMITERS = SENTENCE_DELIMITERS;
						__all__.detect_indent = detect_indent;
						__all__.get_sentences = get_sentences;
						__all__.indent_level = indent_level;
						__all__.lex = lex;
						__all__.lex_line = lex_line;
						__all__.lex_tcbody = lex_tcbody;
						__all__.parse_lawtext = parse_lawtext;
						__all__.re_AppdxStyleLabel = re_AppdxStyleLabel;
						__all__.re_AppdxTableLabel = re_AppdxTableLabel;
						__all__.re_Arg = re_Arg;
						__all__.re_ArticleBody = re_ArticleBody;
						__all__.re_ArticleCaption = re_ArticleCaption;
						__all__.re_ArticleRange = re_ArticleRange;
						__all__.re_BlankLine = re_BlankLine;
						__all__.re_DETECT_INDENT = re_DETECT_INDENT;
						__all__.re_DefaultLine = re_DefaultLine;
						__all__.re_FORCE_EXIT_PARENTHESIS = re_FORCE_EXIT_PARENTHESIS;
						__all__.re_FigLine = re_FigLine;
						__all__.re_LawNum = re_LawNum;
						__all__.re_ParagraphCaption = re_ParagraphCaption;
						__all__.re_ParagraphItemBody = re_ParagraphItemBody;
						__all__.re_SupplProvisionLabel = re_SupplProvisionLabel;
						__all__.re_TC1stLine = re_TC1stLine;
						__all__.re_TCnthLine = re_TCnthLine;
						__all__.skip_parenthesis = skip_parenthesis;
						__all__.py_split = py_split;
						__all__.split_sentences = split_sentences;
					__pragma__ ('</all>')
				}
			}
		}
	);
