const div_dst = '#ttt'

var index = cb_data.source.selected.indices[0];
var text = '';

for (const property in cb_data.source.data) {
  text += `${property}: ${cb_data.source.data[property][index]}`;
}

$(div_dst).text(text);