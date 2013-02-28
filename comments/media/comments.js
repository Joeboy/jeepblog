/* This is currently presumed broken */

function submit_comment() {
    var form_contents = formContents(this);
	var content=queryString(form_contents[0], form_contents[1]);
	var d = doXHR("/comments/post/?xhr", {	method: "POST", 
											mimeType : 'application/x-www-form-urlencoded', 
											sendContent : content,
											headers : {	'Content-Type' : 
														'application/x-www-form-urlencoded'}
						});
	var gotData = function (xhr) {
		var z;
		var data = evalJSONRequest(xhr);
	    new_errors = DIV({'id':'errors'}, null);
		if (data['errors'] || data['valid_captcha'] === false) {
            if (data['errors']) {
    			for (k in data['errors']) {
	    			appendChildNodes(new_errors, P(null, 'Error in '+k+': '+data['errors'][k]));
		    	}
			}
            if (!data['valid_captcha']) {
			    appendChildNodes(new_errors, P(null, 'Your reCAPTCHA entry was invalid'));
            }
            swapDOM($('errors'), new_errors);
            Recaptcha.reload();
			return;
        }
        swapDOM($('errors'), DIV({'id':'errors'}));
		var toggle = false;
		tdiv=DIV({'class':'blogpost-indented', 'id':'comments-list'}, null);
		for (var i=0;i<data.length;i++) {
z = DIV( {'class': (toggle ? 'comment colour1':'comment colour2')}, P(null, STRONG(null,data[i]['username']),' said:'), escapeHTML(data[i]['text']));
			appendChildNodes(tdiv, z);
			toggle = !toggle;
		}
		swapDOM($('comments-list'), tdiv);
        swapDOM($('comment-count'), SPAN({'id':'comment-count'}, data.length));
        Recaptcha.reload();
	};
	var dataFetchFailed = function (err) {
		alert("ajax error");
	};
	d.addCallbacks(gotData, dataFetchFailed);
	return false;
}

function setup_comments() {
	var submit_forms = $$('form.comment_form');
	for (var i=0;i<submit_forms.length;i++) {
		submit_forms[i].onsubmit=submit_comment;
	}
}
addLoadEvent(setup_comments);

