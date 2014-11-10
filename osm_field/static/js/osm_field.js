/* jQuery OSM field
	2014 by Thomas netAction Schmidt for Sinnwerkstatt
	https://www.sinnwerkstatt.com/
	MIT License */
(function($) {
	$.fn.osmfield = function() {

		return this.each(function() {
			// Create HTML elements for osmfield
			var idAttribute = $(this).attr('id');
			var idLatElement = $(this).data('lat-field');
 			var idLonElement = $(this).data('lon-field');

			if (idLatElement === undefined) {
				idLatElement = '#' + idAttribute + '_lat';
			} else {
				idLatElement = '#id_' + idLatElement;
			}

			if (idLonElement === undefined) {
				idLonElement = '#' + idAttribute + '_lon';
			} else {
				idLonElement = '#id_' + idLonElement;
			}

			$(this).addClass('osmfield-input');

			// Create map container when not existent.
			// Wrapper is only for CSS.
			if (!$('#'+idAttribute+'-map').length)
				$(this).before('<div class="osmfield-wrapper"><div id="'+idAttribute+'-map"></div></div>');

			$(this).data('lat-element',$(idLatElement));
			$(this).data('lng-element',$(idLonElement));
			$(this).data('map-element',$('#' + idAttribute+'-map'));
			$(this).data('map-element').addClass('osmfield-map');

			var osmfieldElement = $(this);

			// initialize Leaflet map, tile layer and marker
			var map = L.map(osmfieldElement.data('map-element')[0]).setView([0,0], 15);
			L.tileLayer('https://otile1-s.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.jpg', {
				attribution:
					'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,'+
					' <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>,'+
					' Imagery © <a href="http://www.mapquest.com/">Mapquest</a>',
				maxZoom: 18
			}).addTo(map);
			var marker = L.marker([0,0],{draggable:true}).addTo(map);



			// bubble up the dom to find out language or use 'en' as default
			var lang = osmfieldElement.closest('[lang]').attr('lang');
			if (lang) {
				lang = lang.split('-');
				lang = lang[0];
			} else lang = 'en';
			osmfieldElement.data('language',lang);


			// magic that happens when marker in map is dragged
			(function (osmfieldElement) {
				marker.on('dragend', function(event) {
					var position = event.target.getLatLng();
					map.panTo(position);

					var zoom = map.getZoom();
					var language = osmfieldElement.data('language');
					var url =
						'https://nominatim.openstreetmap.org/reverse?json_callback=?';
					osmfieldElement.data('lat-element').val(position.lat);
					osmfieldElement.data('lng-element').val(position.lng);
					$.getJSON(url,{
							format: 'json',
							lat: position.lat,
							lon: position.lng,
							zoom: zoom,
							addressdetails: 0,
							'accept-language': language
						}, function(data) {
						osmfieldElement.val(data.display_name);
					});
				});
			})(osmfieldElement);


			// User enters something in INPUT field
			osmfieldElement
				.on('propertychange keyup input paste change', function() {
				if ($(this).data('oldvalue')==$(this).val()) return;
				$(this).data('oldvalue',$(this).val());

				function search(nameInputElement) {
					var language = nameInputElement.data('language');
					var url =
						'https://nominatim.openstreetmap.org/search?json_callback=?';
					(function (osmfieldElement) {
						// We could kill previous ajax requests here.
						$.getJSON(url, {
								format: 'json',
								q: nameInputElement.val(),
								addressdetails: 0,
								'accept-language': language
							},function(data) {
							// coordinates found for this address?
							if (data.length) {
								var lat = data[0].lat;
								var lng = data[0].lon;
								var name = data[0].display_name;

								osmfieldElement.data('lat-element').val(lat);
								osmfieldElement.data('lng-element').val(lng);

								var newLatLng = new L.LatLng(lat, lng);
								marker.setLatLng(newLatLng);
								map.panTo(newLatLng);
							} else {
								osmfieldElement.data('map-element').slideUp();
								osmfieldElement.data('lat-element').val('');
								osmfieldElement.data('lng-element').val('');
							}

							// Show map when INPUT has focus and coordinates are known
							if (
								osmfieldElement.is(":focus") &&
								osmfieldElement.data('lat-element').val() &&
								osmfieldElement.data('lng-element').val()
							 ) {
								osmfieldElement.data('map-element').slideDown(function() {
									window.dispatchEvent(new Event('resize'));
								});
							} else {
								osmfieldElement.data('map-element').slideUp();
							}

						});
					})(nameInputElement);
				}

				// Wait 500ms for INPUT updates until Ajax request
				clearTimeout($.data(this, 'timer'));
				var nameInputElement = $(this)
				var wait = setTimeout(function() { search(nameInputElement); }, 500);
				$(this).data('timer', wait);
			});


			// Initialize INPUT, map and data attributes
			osmfieldElement.data('map-element').hide();
			// Use start values if given
			if (
				osmfieldElement.data('lat-element').val() &&
				osmfieldElement.data('lng-element').val()) {
				var newLatLng = new L.LatLng(
					osmfieldElement.data('lat-element').val(),
					osmfieldElement.data('lng-element').val()
				);
				marker.setLatLng(newLatLng);
				map.panTo(newLatLng);
			} else {
				// Maybe OpenStreetMap has coordinates or hide the map
				osmfieldElement.trigger('change');
			}


			// Hide map when clicking outside
			$(document).click(function(event) {
				// A child of INPUT or map was clicked
				var thisosmfield = $(event.target).closest('.osmfield-input, .osmfield-map');
				if(thisosmfield.length) {
					// hide all maps except of this
					if (thisosmfield.hasClass('osmfield-input')) {
						thisosmfield = thisosmfield.data('map-element');
					}
					$('.osmfield-map').not(thisosmfield).slideUp();
				} else {
					// hide all
					$('.osmfield-map').slideUp();
				}
			});


			// Show map when INPUT gets focus and position is known
			(function (osmfieldElement) {
				osmfieldElement.focus(function() {
					if (
						osmfieldElement.data('lat-element').val() &&
						osmfieldElement.data('lng-element').val()
					) {
						osmfieldElement.data('map-element').slideDown(function() {
							window.dispatchEvent(new Event('resize'));
						});
					}
				});
			})(osmfieldElement);

		}); // each osmfield element
	}; // jQuery plugin end
}(jQuery));
