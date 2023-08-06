	(function () {
		var parse_lawtext = __init__ (__world__.lawtext.parse).parse_lawtext;
		var decorate = __init__ (__world__.lawtext.decorate).decorate;
		__pragma__ ('<use>' +
			'lawtext.decorate' +
			'lawtext.parse' +
		'</use>')
		__pragma__ ('<all>')
			__all__.decorate = decorate;
			__all__.parse_lawtext = parse_lawtext;
		__pragma__ ('</all>')
	}) ();
