from twisted.internet.defer import inlineCallbacks

from junebug.router import Router, InvalidRouterConfig, RouterNotFound
from junebug.router.base import InvalidRouterType
from junebug.tests.helpers import JunebugTestBase


class TestRouter(JunebugTestBase):
    @inlineCallbacks
    def setUp(self):
        yield self.start_server()

    def test_creating_uuid(self):
        """If a router isn't given an id, then it should generate one."""
        config = self.create_router_config()
        router = Router(self.api.router_store, self.api.config, config)
        self.assertFalse(router.router_config.get('id') is None)

        config = self.create_router_config(id='test-uuid')
        router = Router(self.api.router_store, self.api.config, config)
        self.assertEqual(router.router_config.get('id'), 'test-uuid')

    @inlineCallbacks
    def test_get_all(self):
        """get_all should return a list of all router ids"""
        self.assertEqual(
            (yield Router.get_all(self.api.router_store)), [])

        config = self.create_router_config(id='test-uuid1')
        yield self.api.router_store.save_router(config)
        self.assertEqual(
            (yield Router.get_all(self.api.router_store)), ['test-uuid1'])

        config = self.create_router_config(id='test-uuid2')
        yield self.api.router_store.save_router(config)
        self.assertEqual(
            (yield Router.get_all(self.api.router_store)),
            ['test-uuid1', 'test-uuid2'])

    @inlineCallbacks
    def test_save(self):
        """save should save the configuration into the router store"""
        config = self.create_router_config()
        router = Router(self.api.router_store, self.api.config, config)

        self.assertEqual((yield self.api.router_store.get_router_list()), [])
        yield router.save()
        self.assertEqual(
            (yield self.api.router_store.get_router_list()),
            [router.router_config['id']])

    @inlineCallbacks
    def test_validate_config(self):
        """validate_config should run the validate config function on the
        router worker class"""
        config = self.create_router_config(config={'test': 'pass'})
        router = Router(self.api.router_store, self.api.config, config)
        yield router.validate_config()

        with self.assertRaises(InvalidRouterConfig):
            config = self.create_router_config(config={'test': 'fail'})
            router = Router(self.api.router_store, self.api.config, config)
            yield router.validate_config()

    @inlineCallbacks
    def test_validate_config_invalid_worker_name(self):
        """If validate_config is given a config with an unknown worker name,
        an appropriate error should be raised."""
        config = self.create_router_config(type='invalid')
        router = Router(self.api.router_store, self.api.config, config)

        with self.assertRaises(InvalidRouterType):
            yield router.validate_config()

    def test_start(self):
        """start should start the router worker with the correct config"""
        config = self.create_router_config()
        router = Router(self.api.router_store, self.api.config, config)
        router.start(self.service)

        router_worker = self.service.namedServices[router.id]
        self.assertEqual(router_worker.parent, self.service)
        self.assertEqual(router_worker.config, config['config'])

    @inlineCallbacks
    def test_stop(self):
        """stop should stop the router worker if it is running"""
        config = self.create_router_config()
        router = Router(self.api.router_store, self.api.config, config)
        router.start(self.service)

        self.assertIn(router.id, self.service.namedServices)

        yield router.stop()

        self.assertNotIn(router.id, self.service.namedServices)

    @inlineCallbacks
    def test_stop_already_stopped(self):
        """Calling stop on a non-running router should not raise any
        exceptions"""

        config = self.create_router_config()
        router = Router(self.api.router_store, self.api.config, config)
        router.start(self.service)

        self.assertIn(router.id, self.service.namedServices)

        yield router.stop()

        self.assertNotIn(router.id, self.service.namedServices)

        yield router.stop()

    @inlineCallbacks
    def test_status(self):
        """status should return the current config of the router"""
        config = self.create_router_config()
        router = Router(self.api.router_store, self.api.config, config)
        status = yield router.status()
        self.assertEqual(status, router.router_config)

    @inlineCallbacks
    def test_from_id(self):
        """from_id should be able to restore a router, given just the id"""
        config = self.create_router_config()
        router = Router(self.api.router_store, self.api.config, config)
        yield router.save()
        router.start(self.api.service)

        restored_router = yield Router.from_id(
            self.api.router_store, self.api.config, self.api.service,
            router.router_config['id'])

        self.assertEqual(router.router_config, restored_router.router_config)
        self.assertEqual(router.router_worker, restored_router.router_worker)

    @inlineCallbacks
    def test_from_id_doesnt_exist(self):
        """If we don't have a router for the specified ID, then we should raise
        the appropriate error"""
        with self.assertRaises(RouterNotFound):
            yield Router.from_id(
                self.api.router_store, self.api.config, self.api.service,
                'bad-router-id')

    @inlineCallbacks
    def test_delete_router(self):
        """Removes the router config from the store"""
        config = self.create_router_config()
        router = Router(self.api.router_store, self.api.config, config)
        yield router.save()
        self.assertEqual(
            (yield self.api.router_store.get_router_list()),
            [router.router_config['id']])

        yield router.delete()
        self.assertEqual((yield self.api.router_store.get_router_list()), [])

    @inlineCallbacks
    def test_delete_router_not_in_store(self):
        """Removing a non-existing router should not result in an error"""
        config = self.create_router_config()
        router = Router(self.api.router_store, self.api.config, config)
        self.assertEqual((yield self.api.router_store.get_router_list()), [])

        yield router.delete()
        self.assertEqual((yield self.api.router_store.get_router_list()), [])
