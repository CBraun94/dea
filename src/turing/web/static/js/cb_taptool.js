const div_dst = '#ttt'

var index = cb_data.source.selected.indices[0];
var text = '';
var dict = {};

for (const property in cb_data.source.data) {
  text += `${property}: ${cb_data.source.data[property][index]}`;
  dict[property] = cb_data.source.data[property][index]
}

$(div_dst).text(text);
$(div_dst).text(JSON.stringify(dict));

$.ajax({
  url: '/graph/select',
  method: 'POST',
  contentType: 'application/json',
  data: JSON.stringify(dict),
  success: function (response) {
    $(div_dst).text(response.output);
  }
});