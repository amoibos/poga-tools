// Global variable to track editor name
var objName;
// Update selection bookmark for each event
function updateSelectionBookmark (ed) {
	ed.updatedSelectionBookmark = ed.selection.getBookmark(1);
}

// Parameters:
// ed_name: Editor/Object Name for textarea
// easycode, smilies, block_html: Settings to display respective toolbar icons
function startEditor(ed_name, easycode, smilies, block_html, spellcheck)
{
	objName = ed_name;
	var button_list1 = "removeformat, fontselect, fontsizeselect, forecolor, |, bold, italic, underline, |, justifyleft, justifycenter, justifyright, |, bullist, numlist, |, outdent, indent";
	var button_list2 = "cut, copy, paste, |, undo, redo, |, link, imagebutton, videobutton, |";
	if (easycode != '') {
		button_list2 += ",wrapcodebutton, wrapquotebutton";
	}
	if (smilies != '') {
		button_list2 += ", emotions";
	}
	if (block_html == '') {
		button_list2 += ", code";
	}
	if (spellcheck != '') {
		button_list2 += ", iespell";
	}
	
	//display dialog content for video option
	var dialogOpts = {
		autoOpen: false,
		modal: true,
		resizable: true,
		minWidth:525,
		show: 'blind',
		title: 'Insert Video',
		buttons: {
			Ok: function() {
				var val = doOK();
				if(val){
				jQuery( this ).dialog( "close" );
				}
			},
			Cancel: function() {
				jQuery( this ).dialog( "close" );
			}
		}
	};
	jQuery('#video_popup').dialog(dialogOpts);
 
	
	//Set value to tinyMCE editor from jquery dialog box and removed data as well as to close dialog box.
	var dialogCodeOpts = {
		autoOpen: false,
		modal: true,
		resizable: true,
		minWidth:525,
		show: 'blind',
		title: 'Insert Code',
		buttons: {
			Ok: function() {
				CodeTags("CODE");
				jQuery('#dialog_input_code_value').val('').empty();
				jQuery( this ).dialog( "close" );
			},
			Cancel: function() {
				jQuery( this ).dialog( "close" );
			}
		}
	};
	jQuery('#code_popup').dialog(dialogCodeOpts);
	
	// Launch new window for supported video sites click 
	jQuery('#video_list a').click(function() {
		window.open( jQuery(this).attr('href') );
		return false;
	});
	
	//display dialog content for smilies option
	var smilie_dialogOpts = {
		autoOpen: false,
		modal: false,
		resizable: true,
		height: 500,
		width: 350,
		show: 'blind',
		title: 'Smilies'
	};
	jQuery("#smilie_popup").dialog(smilie_dialogOpts);

	tinyMCE.init({
			// General options
			mode : "exact",
			theme : "advanced",
			elements : ed_name,
			editor_css : "/css/editor.css",
			gecko_spellcheck : true,
			relative_urls : false,

			// Theme options
			theme_advanced_buttons1 : button_list1,
			theme_advanced_buttons2 : button_list2,
			theme_advanced_buttons3 : "",
			theme_advanced_buttons4 : "",
			theme_advanced_toolbar_location : "top",
			theme_advanced_toolbar_align : "left",
			theme_advanced_resizing : true,
			
			forced_root_block : false,
			force_br_newlines : true,
			force_p_newlines  : false,
			extended_valid_elements : "img[id|style|rel|rev|charset|hreflang|src|class|tabindex]", // for making element valid in tinymce editor 
			
			content_css : "/css/content.css",
			
			setup : function(ed) {
				//Fires before contents is extracted from the editor using for example getContent.
				ed.onBeforeGetContent.add(function(ed, o) {
					//Adds "lightbox" to the "rel" attribute for <img> tag in the active editor for lightbox functionality
					ed.dom.setAttrib(ed.dom.select('img'), 'rel', 'lightbox');
					// Adds a class 'bbc_img' for <img> tag in the active editor for lightbox functionality
					ed.dom.addClass(ed.dom.select('img'), 'bbc_img');
					//Adds "nofollow" to the "rel" attribute for any <a> tags that external link for SEO and preventing spammers
					ed.dom.setAttrib(ed.dom.select('a'), 'rel', 'nofollow');
				});
				// remove line breaks from the HTML source to prevent scripts from inserting <br> tags and save space
				ed.onSaveContent.add(function(ed, o) {
					o.content = cleanEditorHtml(ed.getContent());
				});
			
				// for proper insertion of content from popups/dialogs in IE
				ed.onEvent.add(function (ed, e) {
					ed.updatedSelectionBookmark = ed.selection.getBookmark(1);
				});

				// Add custom buttons
				ed.addButton('videobutton', {
					title : 'Insert Video',
					onclick : function() {
						jQuery('#video_popup').dialog("open");
						return false;
					}
				});
				
				ed.addButton('emotions', {		
					title : 'Insert Smilie',
					onclick : function() {
						// load popup via ajax. skip loading if popup html is already present
						if (jQuery('#smilie_popup').html()) {
							jQuery('#divSmilieInserted').hide();
							jQuery('#smilie_popup').dialog("open");
						} else {
							jQuery('#smilie_popup').load("/cgi/members/smilie.cgi?username="+smilie_user+'&tool='+tool,	function(){
								jQuery('#smilie_popup').dialog("open");
							});
						}
						
						return false;
					}
				});
				
				ed.addButton('imagebutton', {		
					title : 'Insert Image',
					onclick : function() {
						var imagePath = prompt('Please enter the URL of your image:', 'http://');
						if (imagePath != null && imagePath != "") {
							this.execCommand('mceInsertContent', false, '<img rel="lightbox" src='+imagePath+' class="bbc_img">', {skip_undo : 0});
						}
					}
				});
				
				ed.addButton('link', {			
					title : 'Insert Link',
					onclick : function() {
						var sel = this.selection.getContent();

						if (sel == '' || sel == null) {
							alert("Your browser requires that you must select some text for this function to work.");
							return;
						}

						var szURL = prompt("Please enter the URL of your link:", "http://");

						if (szURL != null && szURL != "" && szURL != "http://") {
							this.execCommand("CreateLink", false, szURL);
						} else {
							this.execCommand("UnLink", false, null);
						}
					}
				});
				
				ed.addButton('wrapquotebutton', {			
					title : 'Wrap [QUOTE] tags around selected text',
					onclick : function() {
						wrapTags('QUOTE');
					}
				});
				
				ed.addButton('wrapcodebutton', {			
					title : 'Wrap [CODE] tags around selected text',
					onclick : function() {
						var sel = tinyMCE.activeEditor.selection.getContent();
						
						// wrap tags around selected text or prompt for text
						if (sel) {
							wrapTags('CODE');
						} else {
							jQuery('#code_popup').dialog("open");
						}
					}
				});	
				ed.addButton('iespell', {			
				title : 'Spell Check',
				onclick : function() {
					openSpellChecker(this.getElement());
					}
				});		
				ed.onInit.add(function(ed) {
					jQuery('#adv_toolbar').val('1');
					if (jQuery('#'+ed_name).attr('firstfocus')) {
						ed.focus();
					}
				});
			}
		});
}

function wrapTags (tag) {
	var sel = tinyMCE.activeEditor.selection.getContent();
	var embedTags = "[" + tag +"]"+sel+"[/" + tag +"]";
	tinyMCE.activeEditor.selection.setContent(embedTags);
	
}

function CodeTags (tag) {
	var embedTags = "[" + tag +"]"+ jQuery('#dialog_input_code_value').val() +"[/" + tag +"]";
	tinyMCE.activeEditor.focus();
	tinyMCE.activeEditor.selection.setContent(escapeHTMLtag(embedTags));
}

function escapeHTMLtag(str)
{
	str = str.replace(/&/g, "&amp;");
	str = str.replace(/>/g, "&gt;");
	str = str.replace(/</g, "&lt;");
	str = str.replace(/"/g, "&quot;");
	str = str.replace(/ /g, "&nbsp;");
	str = str.replace(/\n/g, "<br />");
	return str;
}

function doOK() {
	var FileName = jQuery('#dialog_input_value').val();
	if (FileName == '' || FileName == "http://") { 
		alert("Video URL must be specified.");
		jQuery('#dialog_input_value').focus();
		return;
	}
	else if(ValidateURL(FileName)){
		var embedPath = "[video]"+FileName+"[/video]";
		var ed = tinyMCE.get(objName);
		ed.selection.moveToBookmark(ed.updatedSelectionBookmark);
		tinyMCE.execCommand("mceInsertContent", false, embedPath);
		return 1;
	}
	else {
		alert("Please enter a valid URL. Supported videos include Hulu, YouTube, Vimeo, Dailymotion, Metacafe, Google, Facebook. ");
		jQuery('#dialog_input_value').focus();
		return;
	}
}

// validate video URL
function ValidateURL(videoPath) {
	var regex = /youtube|youtu.be|hulu|vimeo|dailymotion|metacafe|facebook|google/ig;
	if (regex.test(videoPath)) {
		return true;
	} 
	return false;
}

function cleanEditorHtml (data) {
	var data = removeLightboxAnchor(data);
	data = removeSmiliesLightbox(data);
	data = data.replace(/(\r\n|\n|\r)/gm,"");
	return data;
}

// to remove lightbox if anchors
function removeLightboxAnchor(rawHTML)
{
	var doc = document.createElement("div");
	doc.innerHTML = rawHTML;	
	var images = doc.getElementsByTagName("img");
	for (var i=0; i<images.length; i++) {
		// getting parent node of image tag
		var obj_parent = images[i].parentNode;
		// checking for anchor tag
		if(obj_parent.tagName=='A' || obj_parent.tagName=='a') {
			// removing rel attribute from image if it is nested within anchors
			images[i].removeAttribute("rel");
		}
	}
	return doc.innerHTML;
}

// to remove lightbox if there are smilies with images
function removeSmiliesLightbox(rawHTML)
{
	var doc = document.createElement("div");
	doc.innerHTML = rawHTML;	
	var images = doc.getElementsByTagName("img");
	for (var i=0; i<images.length; i++) {
		// checking for smilies image class to remove rel attribute
		if(jQuery(images[i]).hasClass("emoticon")){
			images[i].removeAttribute("rel");
		}	
	}
	return doc.innerHTML; 	
}

