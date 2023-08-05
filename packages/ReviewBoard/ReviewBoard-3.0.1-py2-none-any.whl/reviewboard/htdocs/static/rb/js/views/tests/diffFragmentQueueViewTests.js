'use strict';

suite('rb/views/DiffFragmentQueueView', function () {
    var URL_PREFIX = '/r/123/_fragments/diff-comments/';

    var fragmentQueue = void 0;

    beforeEach(function () {
        fragmentQueue = new RB.DiffFragmentQueueView({
            containerPrefix: 'container1',
            reviewRequestPath: '/r/123/',
            queueName: 'diff_fragments'
        });
    });

    describe('Diff fragment loading', function () {
        var $container1 = void 0;
        var $container2 = void 0;
        var $container3 = void 0;

        beforeEach(function () {
            $container1 = $('<div id="container1_123"/>').appendTo(window.$testsScratch);
            $container2 = $('<div id="container1_124"/>').appendTo(window.$testsScratch);
            $container3 = $('<div id="container1_125"/>').appendTo(window.$testsScratch);

            fragmentQueue.queueLoad('123', 'key1');
            fragmentQueue.queueLoad('124', 'key1');
            fragmentQueue.queueLoad('125', 'key2');
        });

        it('Fragment queueing', function () {
            var queue = fragmentQueue._queue;

            expect(queue.length).not.toBe(0);

            expect(queue.key1.length).toBe(2);
            expect(queue.key1).toContain({
                commentID: '123',
                onFragmentRendered: null
            });
            expect(queue.key1).toContain({
                commentID: '124',
                onFragmentRendered: null
            });
            expect(queue.key2.length).toBe(1);
            expect(queue.key2).toContain({
                commentID: '125',
                onFragmentRendered: null
            });
        });

        it('Batch loading', function () {
            var urls = [URL_PREFIX + '123,124/', URL_PREFIX + '125/'];

            spyOn($, 'ajax').and.callFake(function (options) {
                var url = options.url;

                if (url === urls[0]) {
                    var html1 = '<span>Comment 1</span>';
                    var html2 = '<span>Comment 2</span>';

                    options.success('123\n' + (html1.length + '\n') + html1 + '124\n' + (html2.length + '\n') + html2);
                } else if (url === urls[1]) {
                    var html = '<span>Comment 3</span>';
                    options.success('125\n' + html.length + '\n' + html);
                } else {
                    fail('Unexpected URL ' + url);
                }
            });

            fragmentQueue.loadFragments();

            expect($.ajax.calls.count()).toBe(2);

            expect($container1.data('diff-fragment-view')).toBeTruthy();
            expect($container1.html()).toBe('<span>Comment 1</span>');

            expect($container2.data('diff-fragment-view')).toBeTruthy();
            expect($container2.html()).toBe('<span>Comment 2</span>');

            expect($container3.data('diff-fragment-view')).toBeTruthy();
            expect($container3.html()).toBe('<span>Comment 3</span>');
        });

        it('With saved fragments', function () {
            var urls = [URL_PREFIX + '124/', URL_PREFIX + '125/'];

            spyOn($, 'ajax').and.callFake(function (options) {
                var url = options.url;

                if (url === urls[0]) {
                    var html = '<span>New comment 2</span>';
                    options.success('124\n' + html.length + '\n' + html);
                } else if (url === urls[1]) {
                    var _html = '<span>New comment 3</span>';
                    options.success('125\n' + _html.length + '\n' + _html);
                } else {
                    fail('Unexpected URL ' + url);
                }
            });

            /*
             * We'll set up the first two containers, but leave the third as
             * completely new. Both the unsaved pre-loaded container (2) and
             * the new container (3) will be loaded.
             */
            $container1.html('<span>Comment 1</span>').data('diff-fragment-view', new RB.DiffFragmentView());

            $container2.html('<span>Comment 2</span>').data('diff-fragment-view', new RB.DiffFragmentView());

            /*
             * We're going to save 123 and 125 (which is not loaded). Only
             * 123 will actually be saved.
             */
            fragmentQueue.saveFragment('123');
            fragmentQueue.saveFragment('125');

            fragmentQueue.loadFragments();

            expect($.ajax.calls.count()).toBe(2);

            expect($container1.data('diff-fragment-view')).toBeTruthy();
            expect($container1.html()).toBe('<span>Comment 1</span>');

            expect($container2.data('diff-fragment-view')).toBeTruthy();
            expect($container2.html()).toBe('<span>New comment 2</span>');

            expect($container3.data('diff-fragment-view')).toBeTruthy();
            expect($container3.html()).toBe('<span>New comment 3</span>');

            expect(fragmentQueue._saved).toEqual({});
        });
    });
});

//# sourceMappingURL=diffFragmentQueueViewTests.js.map