// TODO: README.md
// TODO: License

(function($) {
	$.fn.osmfield = function() {

		return this.each(function() {
			// Create HTML elements for osmfield
			$(this)
				.addClass('osmfield-address')
				.wrap('<span class="osmfield-wrapper"></span>')
				.parent()
				.append('<div class="osmfield-map"></div>');

			var osmfieldElement = $(this).parent();

			// initialize Leaflet map, tile layer and marker
			var map = L.map(osmfieldElement.find('.osmfield-map')[0]).setView([0,0], 15);
			L.tileLayer('http://a.tiles.mapbox.com/v3/examples.map-9ijuk24y/{z}/{x}/{y}.png', {
				attribution:
					'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,'+
					' <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>,'+
					' Imagery © <a href="http://mapbox.com">Mapbox</a>',
				maxZoom: 18
			}).addTo(map);
			var marker = L.marker([0,0],{draggable:true}).addTo(map);



			// bubble up the dom to find out language or use 'en' as default
			var lang = osmfieldElement.find('.osmfield-address').closest('[lang]').attr('lang');
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
					osmfieldElement.find('.osmfield-address').attr('data-osmfield-lat',position.lat);
					osmfieldElement.find('.osmfield-address').attr('data-osmfield-lng',position.lng);
					$.getJSON(url,{
							format: 'json',
							lat: position.lat,
							lon: position.lng,
							zoom: zoom,
							addressdetails: 0,
							'accept-language': language
						}, function(data) {
						osmfieldElement.find('input.osmfield-address').val(data.display_name);
					});
				});
			})(osmfieldElement);


			// User enters something in INPUT field
			osmfieldElement.find('input.osmfield-address')
				.on('propertychange keyup input paste change', function() {
				if ($(this).data('oldvalue')==$(this).val()) return;
				$(this).data('oldvalue',$(this).val());

				function search(nameInputElement) {
					var language = nameInputElement.closest('.osmfield-wrapper').data('language');
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

								osmfieldElement.find('.osmfield-address').attr('data-osmfield-lat',lat);
								osmfieldElement.find('.osmfield-address').attr('data-osmfield-lng',lng);

								var newLatLng = new L.LatLng(lat, lng);
								marker.setLatLng(newLatLng);
								map.panTo(newLatLng);
							} else {
								osmfieldElement.find('.osmfield-map').slideUp();
								osmfieldElement.find('.osmfield-address').removeAttr('data-osmfield-lat');
								osmfieldElement.find('.osmfield-address').removeAttr('data-osmfield-lng');
							}

							// Show map when INPUT has focus and coordinates are known
							if (
								osmfieldElement.find('.osmfield-address').is(":focus") &&
								osmfieldElement.find('.osmfield-address').attr('data-osmfield-lat') &&
								osmfieldElement.find('.osmfield-address').attr('data-osmfield-lng')
							 ) {
								osmfieldElement.find('.osmfield-map').slideDown();
							} else {
								osmfieldElement.find('.osmfield-map').slideUp();
							}

						});
					})(nameInputElement.parent());
				}

				// Wait 500ms for INPUT updates until Ajax request
				clearTimeout($.data(this, 'timer'));
				var nameInputElement = $(this)
				var wait = setTimeout(function() { search(nameInputElement); }, 500);
				$(this).data('timer', wait);
			});


			// Initialize INPUT, map and data attributes
			osmfieldElement.find('.osmfield-map').hide();
			// Use start values if given
			if (
				osmfieldElement.find('.osmfield-address').attr('data-osmfield-lat') &&
				osmfieldElement.find('.osmfield-address').attr('data-osmfield-lng')) {
				var newLatLng = new L.LatLng(
					osmfieldElement.find('.osmfield-address').attr('data-osmfield-lat'),
					osmfieldElement.find('.osmfield-address').attr('data-osmfield-lng')
				);
				marker.setLatLng(newLatLng);
				map.panTo(newLatLng);
			} else {
				// Maybe OpenStreetMap has coordinates or hide the map
				osmfieldElement.find('input.osmfield-address').trigger('change');
			}


			// Hide map when clicking outside
			$(document).click(function(event) {
				var thisosmfield = $(event.target).closest('.osmfield-wrapper');
				if(thisosmfield.length) {
					// hide all maps except of this
					$('.osmfield-map').not(thisosmfield.find('.osmfield-map')).slideUp();
				} else {
					// hide all
					$('.osmfield-map').slideUp();
				}
			});


			// Show map when INPUT gets focus and position is known
			(function (osmfieldElement) {
				osmfieldElement.find('.osmfield-address').focus(function() {
					if (
						osmfieldElement.find('.osmfield-address').attr('data-osmfield-lat') &&
						osmfieldElement.find('.osmfield-address').attr('data-osmfield-lng')
					) {
						osmfieldElement.find('.osmfield-map').slideDown();
					}
				});
			})(osmfieldElement);

		}); // each osmfield element
	}; // jQuery plugin end
}(jQuery));
