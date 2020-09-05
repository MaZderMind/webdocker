// Message Handling
$(function () {
    const ws = new WebSocket('ws://' + document.location.host + '/ws');
    const $log = $('.log');
    const $prompt = $('.prompt-input');

    ws.onmessage = function (event) {
        $log.append(event.data);
    };

    $prompt.on('keydown', function (event) {
        if (event.keyCode !== 13) {
            return
        }

        ws.send($prompt.val())
        $prompt.val('');
        $prompt.focus();
    });
});

// Focus Handling
$(function () {
    const $prompt = $('.prompt-input');

    $('body').on('click', function () {
        $prompt.focus();
    })

    $('.log').on('click', function (event) {
        event.stopPropagation();
    })
});
