	__nest__ (
		__all__,
		'lawtext.decorate', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var re = {};
					__nest__ (re, '', __init__ (__world__.re));
					var re_JpNum = re.compile ('^(?P<s1000>(?P<d1000>\\S*)千)?(?P<s100>(?P<d100>\\S*)百)?(?P<s10>(?P<d10>\\S*)十)?(?P<d1>\\S*)?$');
					var jpnum_digits = dict ({'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9});
					var parse_jpnum = function (text) {
						var match = re_JpNum.match (text);
						if (match) {
							var d1000 = jpnum_digits.py_get (match.group (2), (match.group (1) ? 1 : 0));
							var d100 = jpnum_digits.py_get (match.group (4), (match.group (3) ? 1 : 0));
							var d10 = jpnum_digits.py_get (match.group (6), (match.group (5) ? 1 : 0));
							var d1 = jpnum_digits.py_get (match.group (7), 0);
							return str (((d1000 * 1000 + d100 * 100) + d10 * 10) + d1);
						}
						return null;
					};
					var parse_romannum = function (text) {
						var num = 0;
						var __iterable0__ = enumerate (text);
						for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
							var __left0__ = __iterable0__ [__index0__];
							var i = __left0__ [0];
							var char = __left0__ [1];
							if (__in__ (char, tuple (['i', 'I', 'ｉ', 'Ｉ']))) {
								if (i + 1 < len (text) && __in__ (text [i + 1], tuple (['x', 'X', 'ｘ', 'Ｘ']))) {
									num--;
								}
								else {
									num++;
								}
							}
							if (__in__ (char, tuple (['x', 'X', 'ｘ', 'Ｘ']))) {
								num += 10;
							}
						}
						return num;
					};
					var eras = dict ({'明治': 'Meiji', '大正': 'Taisho', '昭和': 'Showa', '平成': 'Heisei'});
					var re_LawTypes = list ([tuple ([re.compile ('^法律$'), 'Act']), tuple ([re.compile ('^政令$'), 'CabinetOrder']), tuple ([re.compile ('^勅令$'), 'ImperialOrder']), tuple ([re.compile ('^\\S*[^政勅]令$'), 'MinisterialOrdinance']), tuple ([re.compile ('^\\S*規則$'), 'Rule'])]);
					var re_LawNum = re.compile ('(?P<era>\\S+?)(?P<year>[一二三四五六七八九十]+)年(?P<law_type>\\S+?)第(?P<num>[一二三四五六七八九十百千]+)号');
					var decorate_law = function (el) {
						el ['attr'] ['Lang'] = 'ja';
						var __iterable0__ = el ['children'];
						for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
							var subel = __iterable0__ [__index0__];
							if (subel ['tag'] == 'LawNum' && len (subel ['children'])) {
								var law_num = subel ['children'] [0];
								var match = re_LawNum.match (law_num);
								if (match) {
									var era = eras.py_get (match.group (1));
									if (era) {
										el ['attr'] ['Era'] = era;
									}
									var year = parse_jpnum (match.group (2));
									if (year) {
										el ['attr'] ['Year'] = str (year);
									}
									var __iterable1__ = re_LawTypes;
									for (var __index1__ = 0; __index1__ < __iterable1__.length; __index1__++) {
										var __left0__ = __iterable1__ [__index1__];
										var re_LawType = __left0__ [0];
										var law_type = __left0__ [1];
										var law_type_match = re_LawType.match (match.group (3));
										if (law_type_match) {
											el ['attr'] ['LawType'] = law_type;
											break;
										}
									}
									var num = parse_jpnum (match.group (4));
									if (num) {
										el ['attr'] ['Num'] = num;
									}
								}
							}
						}
					};
					var WIDE_NUMS = dict ({'０': '0', '１': '1', '２': '2', '３': '3', '４': '4', '５': '5', '６': '6', '７': '7', '８': '8', '９': '9'});
					var replace_wide_num = function (text) {
						var ret = text;
						var __iterable0__ = WIDE_NUMS.py_items ();
						for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
							var __left0__ = __iterable0__ [__index0__];
							var wide = __left0__ [0];
							var narrow = __left0__ [1];
							var ret = ret.py_replace (wide, narrow);
						}
						return ret;
					};
					var re_NamedNum = re.compile ('^(?P<circle>○?)第?(?P<num>[一二三四五六七八九十百千]+)\\S*?(?P<branch>の\\S+)?$');
					var IROHA_CHARS = 'イロハニホヘトチリヌルヲワカヨタレソツネナラムウヰノオクヤマケフコエテアサキユメミシヱヒモセスン';
					var re_ItemNum = re.compile ('^\\D*(?P<num>\\d+)\\D*$');
					var parse_named_num = function (text) {
						var nums_group = list ([]);
						var __iterable0__ = text.py_replace ('及び', '、').py_replace ('から', '、').py_replace ('まで', '').py_replace ('～', '、').py_replace ('・', '、').py_split ('、');
						for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
							var subtext = __iterable0__ [__index0__];
							var match = re_NamedNum.match (subtext);
							if (match) {
								var nums = list ([parse_jpnum (match.group (2))]);
								if (match.group (3)) {
									nums.extend (function () {
										var __accu0__ = [];
										var __iterable1__ = match.group (3).py_split ('の');
										for (var __index1__ = 0; __index1__ < __iterable1__.length; __index1__++) {
											var b = __iterable1__ [__index1__];
											if (b) {
												__accu0__.append (parse_jpnum (b));
											}
										}
										return __accu0__;
									} ());
								}
								nums_group.append ('_'.join (map (str, nums)));
								continue;
							}
							var iroha_char_detected = false;
							var __iterable1__ = enumerate (IROHA_CHARS);
							for (var __index1__ = 0; __index1__ < __iterable1__.length; __index1__++) {
								var __left0__ = __iterable1__ [__index1__];
								var i = __left0__ [0];
								var char = __left0__ [1];
								if (__in__ (char, subtext)) {
									nums_group.append (str (i + 1));
									var iroha_char_detected = true;
									break;
								}
							}
							if (!(iroha_char_detected)) {
								var subtext = replace_wide_num (subtext);
								var match = re_ItemNum.match (subtext);
								if (match) {
									nums_group.append (match.group (1));
									continue;
								}
							}
							var roman_num = parse_romannum (subtext);
							if (roman_num) {
								nums_group.append (str (roman_num));
							}
						}
						return ':'.join (nums_group);
					};
					var decorate_toc_article_group = function (el) {
						el ['attr'] ['Delete'] = 'false';
						var __iterable0__ = el ['children'];
						for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
							var subel = __iterable0__ [__index0__];
							if (__in__ (subel ['tag'], tuple (['PartTitle', 'ChapterTitle', 'SectionTitle', 'SubsectionTitle', 'DivisionTitle', 'ArticleTitle'])) && len (subel ['children'])) {
								var body = subel ['children'] [0];
								var num = parse_named_num (body.py_split () [0]);
								if (num) {
									el ['attr'] ['Num'] = num;
								}
							}
						}
					};
					var decorate_article_group = function (el) {
						el ['attr'] ['Delete'] = 'false';
						el ['attr'] ['Hide'] = 'false';
						var __iterable0__ = el ['children'];
						for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
							var subel = __iterable0__ [__index0__];
							if (__in__ (subel ['tag'], tuple (['PartTitle', 'ChapterTitle', 'SectionTitle', 'SubsectionTitle', 'DivisionTitle', 'ArticleTitle'])) && len (subel ['children'])) {
								var body = subel ['children'] [0];
								var num = parse_named_num (body.py_split () [0]);
								if (num) {
									el ['attr'] ['Num'] = num;
								}
							}
						}
					};
					var decorate_article = function (el) {
						el ['attr'] ['Delete'] = 'false';
						el ['attr'] ['Hide'] = 'false';
						var __iterable0__ = el ['children'];
						for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
							var subel = __iterable0__ [__index0__];
							if (subel ['tag'] == 'ArticleTitle' && len (subel ['children'])) {
								var body = subel ['children'] [0];
								var num = parse_named_num (body.py_split () [0]);
								if (num) {
									el ['attr'] ['Num'] = num;
								}
							}
						}
					};
					var decorate_paragraph = function (el) {
						el ['attr'] ['Hide'] = 'false';
						el ['attr'] ['OldStyle'] = 'false';
						var __iterable0__ = el ['children'];
						for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
							var subel = __iterable0__ [__index0__];
							if (subel ['tag'] == 'ParagraphNum') {
								if (len (subel ['children'])) {
									var paragraph_num = subel ['children'] [0];
									var num = parse_named_num (paragraph_num);
								}
								else {
									var num = '1';
								}
								if (num) {
									el ['attr'] ['Num'] = num;
								}
							}
						}
					};
					var decorate_item = function (el) {
						el ['attr'] ['Delete'] = 'false';
						el ['attr'] ['Hide'] = 'false';
						var __iterable0__ = el ['children'];
						for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
							var subel = __iterable0__ [__index0__];
							if (__in__ (subel ['tag'], tuple (['ItemTitle', 'Subitem1Title', 'Subitem2Title', 'Subitem3Title', 'Subitem4Title', 'Subitem5Title', 'Subitem6Title', 'Subitem7Title', 'Subitem8Title', 'Subitem9Title', 'Subitem10Title']))) {
								var body = subel ['children'] [0];
								var num = parse_named_num (body.py_split () [0]);
								if (num) {
									el ['attr'] ['Num'] = num;
								}
							}
						}
					};
					var decorate_column_sentence_group = function (el) {
						var column_sentences = list ([]);
						var __iterable0__ = el ['children'];
						for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
							var subel = __iterable0__ [__index0__];
							if (__in__ (subel ['tag'], tuple (['Column', 'Sentence']))) {
								column_sentences.append (subel);
							}
						}
						var proviso_nums = list ([]);
						var __iterable0__ = enumerate (column_sentences);
						for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
							var __left0__ = __iterable0__ [__index0__];
							var i = __left0__ [0];
							var subel = __left0__ [1];
							if (len (column_sentences) > 1) {
								subel ['attr'] ['Num'] = str (i + 1);
							}
							if (subel ['tag'] == 'Column') {
								subel ['attr'] ['LineBreak'] = 'false';
							}
							if (subel ['tag'] == 'Sentence' && len (subel ['children']) && (subel ['children'] [0].startswith ('ただし、') || subel ['children'] [0].startswith ('但し、'))) {
								proviso_nums.append (i);
							}
						}
						if (len (proviso_nums)) {
							var __iterable0__ = enumerate (column_sentences);
							for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
								var __left0__ = __iterable0__ [__index0__];
								var i = __left0__ [0];
								var subel = __left0__ [1];
								subel ['attr'] ['Function'] = (__in__ (i, proviso_nums) ? 'proviso' : 'main');
							}
						}
					};
					var decorate_sentence = function (el) {
						el ['attr'] ['WritingMode'] = 'vertical';
					};
					var decorate_table = function (el) {
						el ['attr'] ['WritingMode'] = 'vertical';
					};
					var decorate_table_column = function (el) {
						el ['attr'] ['BorderTop'] = 'solid';
						el ['attr'] ['BorderRight'] = 'solid';
						el ['attr'] ['BorderBottom'] = 'solid';
						el ['attr'] ['BorderLeft'] = 'solid';
					};
					var appdx_table_title = function (el) {
						el ['attr'] ['WritingMode'] = 'vertical';
					};
					var decorate = function (el) {
						if (el ['tag'] == 'Law') {
							decorate_law (el);
						}
						else if (__in__ (el ['tag'], tuple (['TOCPart', 'TOCChapter', 'TOCSection', 'TOCSubsection', 'TOCDivision', 'TOCArticle']))) {
							decorate_toc_article_group (el);
						}
						else if (__in__ (el ['tag'], tuple (['Part', 'Chapter', 'Section', 'Subsection', 'Division']))) {
							decorate_article_group (el);
						}
						else if (el ['tag'] == 'Article') {
							decorate_article (el);
						}
						else if (el ['tag'] == 'Paragraph') {
							decorate_paragraph (el);
						}
						else if (el ['tag'] == 'Sentence') {
							decorate_sentence (el);
						}
						else if (__in__ (el ['tag'], tuple (['Item', 'Subitem1', 'Subitem2', 'Subitem3', 'Subitem4', 'Subitem5', 'Subitem6', 'Subitem7', 'Subitem8', 'Subitem9', 'Subitem10']))) {
							decorate_item (el);
						}
						else if (__in__ (el ['tag'], tuple (['ParagraphSentence', 'ItemSentence', 'Subitem1Sentence', 'Subitem2Sentence', 'Subitem3Sentence', 'Subitem4Sentence', 'Subitem5Sentence', 'Subitem6Sentence', 'Subitem7Sentence', 'Subitem8Sentence', 'Subitem9Sentence', 'Subitem10Sentence', 'Column']))) {
							decorate_column_sentence_group (el);
						}
						else if (el ['tag'] == 'Table') {
							decorate_table (el);
						}
						else if (el ['tag'] == 'TableColumn') {
							decorate_table_column (el);
						}
						else if (el ['tag'] == 'AppdxTableTitle') {
							appdx_table_title (el);
						}
						var __iterable0__ = el ['children'];
						for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
							var subel = __iterable0__ [__index0__];
							if (isinstance (subel, str)) {
								continue;
							}
							decorate (subel);
						}
					};
					__pragma__ ('<use>' +
						're' +
					'</use>')
					__pragma__ ('<all>')
						__all__.IROHA_CHARS = IROHA_CHARS;
						__all__.WIDE_NUMS = WIDE_NUMS;
						__all__.appdx_table_title = appdx_table_title;
						__all__.decorate = decorate;
						__all__.decorate_article = decorate_article;
						__all__.decorate_article_group = decorate_article_group;
						__all__.decorate_column_sentence_group = decorate_column_sentence_group;
						__all__.decorate_item = decorate_item;
						__all__.decorate_law = decorate_law;
						__all__.decorate_paragraph = decorate_paragraph;
						__all__.decorate_sentence = decorate_sentence;
						__all__.decorate_table = decorate_table;
						__all__.decorate_table_column = decorate_table_column;
						__all__.decorate_toc_article_group = decorate_toc_article_group;
						__all__.eras = eras;
						__all__.jpnum_digits = jpnum_digits;
						__all__.parse_jpnum = parse_jpnum;
						__all__.parse_named_num = parse_named_num;
						__all__.parse_romannum = parse_romannum;
						__all__.re_ItemNum = re_ItemNum;
						__all__.re_JpNum = re_JpNum;
						__all__.re_LawNum = re_LawNum;
						__all__.re_LawTypes = re_LawTypes;
						__all__.re_NamedNum = re_NamedNum;
						__all__.replace_wide_num = replace_wide_num;
					__pragma__ ('</all>')
				}
			}
		}
	);
