var index = cb_data.source.selected.indices[0];
var dict = {};

for (const property in cb_data.source.data) {
  dict[property] = cb_data.source.data[property][index]
}

$.ajax({
  url: '/graph/select',
  method: 'POST',
  contentType: 'application/json',
  data: JSON.stringify(dict),
  success: function (response) {
    console.log(response)
  }
});