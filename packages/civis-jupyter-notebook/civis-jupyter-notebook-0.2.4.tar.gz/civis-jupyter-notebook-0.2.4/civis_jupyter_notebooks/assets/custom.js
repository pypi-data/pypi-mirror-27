define(['base/js/namespace'], function(Jupyter){
    Jupyter._target = '_self';
});

$('#new_notebook').hide();
$('#open_notebook').hide();
$('#copy_notebook').hide();
$('#rename_notebook').hide();
$('#save_checkpoint').hide();
$('#restore_checkpoint').hide();
$('#kill_and_exit').hide();
$('#trust_notebook').hide();
$('#file_menu .divider').each(function(i, el) { $(el).hide(); });
$('#login_widget').hide();
$('#kernel_menu .divider').hide();
$('#menu-change-kernel').hide();

if (window.location.pathname == '/notebooks/notebook.ipynb') {
  // Disable a link back to the tree view
  $('#header-container').hide();
  $('a[title="dashboard"]').attr('href', '#');
} else {
  $('#header-container').show();
  $('a[title="dashboard"]').attr('href', '/notebooks/notebook.ipynb');
}
$('a[title="dashboard"]').attr('target', '_self');
$('a[title="dashboard"]').attr('title', 'notebook');

$('#maintoolbar-container').append('<div class="btn-group"><button class="btn btn-default" title="open terminal" onclick="window.location.href = \'/terminals/1\'"><i class="fa fa-terminal" aria-hidden="true"></i></button></div>')

window.setTimeout(function() {
  $("#notebook_name").off();
  require(['base/js/events'], function(events) {
    events.on('set_dirty.Notebook', function(evt, data) {
      window.parent.postMessage({text: 'mark_dirty', dirty: data.value}, '*');
    })
  });
}, 1200);

