'use strict';

suite('rb/ui/managers/NotificationManagerModel', function () {
    beforeEach(function () {
        RB.NotificationManager.instance.setup();
    });

    describe('Notification Manager', function () {
        it('Calls external API', function () {
            spyOn(RB.NotificationManager, 'Notification').and.returnValue({
                close: function close() {
                    return true;
                }
            });

            RB.NotificationManager.instance.notify({
                title: 'Test',
                body: 'This is a Test'
            });

            expect(RB.NotificationManager.Notification).toHaveBeenCalled();
        });

        it('Should notify', function () {
            RB.NotificationManager.instance._canNotify = true;
            spyOn(RB.NotificationManager.instance, '_haveNotificationPermissions').and.returnValue(true);

            expect(RB.NotificationManager.instance.shouldNotify()).toBe(true);
        });

        it('Should not notify due to user permissions', function () {
            RB.NotificationManager.instance._canNotify = false;
            spyOn(RB.NotificationManager.instance, '_haveNotificationPermissions').and.returnValue(true);

            expect(RB.NotificationManager.instance.shouldNotify()).toBe(false);
        });

        it('Should not notify due to browser permissions', function () {
            RB.NotificationManager.instance._canNotify = true;
            spyOn(RB.NotificationManager.instance, '_haveNotificationPermissions').and.returnValue(false);

            expect(RB.NotificationManager.instance.shouldNotify()).toBe(false);
        });
    });
});

//# sourceMappingURL=notificationManagerTests.js.map