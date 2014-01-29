jQuery(document).ready(function(){
    jQuery("a[rel^='prettyPhoto']").prettyPhoto({
        social_tools: ''
    });
	var csrfd = {}
	csrfd[CSRFN] = CSRFV;
	$.ajaxSetup({
	    dataType: "text json",
	    contentType: "application/x-www-form-urlencoded; charset=UTF-8",
	    data: csrfd,
	});
	
	var cat_inp = $("#id_category");
	var file_inp = $('#id_images-file')
	//console.log(cat_inp);

	var but = $('<input>').addClass('btn btn-mini').prop('type','button').val("Добавить категорию").click(function(){
		var div = $('<div>').text('Добавить категорию').css('background-color','white')
		.width('400')
		.height('200');
				
	
		var txt = $('<input>').appendTo(div).change(function(e){
			var val = $(this).val();
			var d = {'name': val}
			d[CSRFN] = CSRFV;
			$.ajax({url: window.category_add_url,
					type:'post',
					dataType:'json',
					data:d,
					success:function(result){
						$('<option>').val(result.id).text(result.name).appendTo(cat_inp);
						div.remove();
					
					}
				
				})
		
				
			return false;
		  })
		  var cancel = $('<button>').text('Отмена')
		  						  .appendTo(div)
								  .addClass('btn btn-mini btn-danger')
								  .click( function(e) {
										  txt.remove();
										  cancel.remove();
										  div.remove();
									  })
		  var create = $('<button>').text('Создать')
		  						  .appendTo(div)
								  .addClass('btn btn-mini btn-primary')
								  .click( function(e) {
						  			var val = txt.val();
						  			var d = {'name': val}
						  			d[CSRFN] = CSRFV;
						  			$.ajax({url: window.category_add_url,
						  					type:'post',
						  					dataType:'json',
						  					data:d,
						  					success:function(result){
						  						$('<option>').val(result.id).text(result.name).appendTo(cat_inp);
						  						div.remove();
					
						  					}
				
						  				})
		
				
						  			return false;
									  
									  })
				  
		var off = cat_inp.offset();
		//console.log(off);
		div.appendTo($('body')).css({position:'absolute', top:off.top, left:off.left } )
		
		
	})
	but.insertAfter(cat_inp);
	
	
	
	$('input.remove-button').val('удалить').click(function (evt) {
		var id = $(this).attr('img_id')
		var par = $(this).parent();
		

		$.ajax({
			type: "POST",
			url: window.gallery_delete_url,
			data: { id: id },
			complete: function (data)
			{
				var response = jQuery.parseJSON(data.responseText)
				if (response.success){
					par.parent().remove();
					//console.log("response success");
				}
			}
		});
	})

	var h2 = $('<h4>').text('Выбрать архив с фотографиями').insertAfter(file_inp)
	$('<input>').prop('type','file').insertAfter(h2)
				.css('display','block')
	.change(function(evt){
		
		
		var f = this.files[0]
		var name = f.name
		var size = f.size
		var cont = $('<div>').insertAfter($(this))
		$(this).hide()
		var id = 'id_images'
		
		var loading = jQuery('#'+id+'-loading')
		var list = jQuery('#'+id+'-thumbnails')
		
		
    
		$('<span>').css('padding-left','40px').text(name).appendTo(cont)
		$('<span>').css('padding-left','40px').text((Math.round((size / 1024) * 100) /100) + ' Kb').appendTo(cont)
		
		prog = $('<span>').css('padding-left','40px').text("0%").appendTo(cont)
		$('<input>').css('padding-left','40px').prop('type','button').val('Начать загрузку').click(function(e){
			val = cat_inp.val()
			if( val ){
		
		    	loading.appendTo(list)
		    	loading.show()
				
				
		        var xhr = new XMLHttpRequest()
		        var fd = new FormData();
        
				
				var loadend = function(e){
					//this.result
					var val = JSON.parse(this.response)
					if (val.success){
						
						// console.log(val)
						for(i=0 ;i<val.file_ids.length; i++){
							var fid  = val.file_ids[i];
							var turl = val.thumb_urls[i]
							
							jQuery('#'+id+'-errors-block').hide()
					        var html = '<div class="gallery-image" onclick="GalleryImageDelete(\''+id+'\', \''+fid+'\')" onmouseover="showButton(\''+id+'\', \''+fid+'\')" onmouseout="hideButton(\''+id+'\', \''+fid+'\')">'
					        html += '<div><img id="'+id+'-img'+fid+'" src="'+ turl+'"></div>'
			        		var img = jQuery(html)
							//console.log(img, list)
							img.appendTo(list)
							
							addValue(id, fid)
						}
					}
					loading.hide();
					
					
				}
		
		        fd.append('file', f)
		        // fd.append(CSRFN, CSRFV)
				
		        xhr.upload.addEventListener('progress', function(e){
					console.log(e.lengthComputable)
					var p = 100 *  (e.loaded/ e.total)
					prog.text( p + '%')
				},false)
				
				// xhr.onprogress=function(e){
				//	console.log("DP",e);
				//}
		        xhr.onloadend = loadend
		
		        xhr.open("POST", zip_upload_url, true)
				xhr.setRequestHeader("X-CSRFToken", CSRFV );
		        xhr.send(fd)
				
			}else{
				alert('надо выбрать категорию перед началом загрузки')
			}
		}).appendTo(cont)
		
		
		
		
		evt.preventDefault()
		evt.stopPropagation()
		
	})
	
	
	
});