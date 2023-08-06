from eryx_deploy.assets.language_environments.ruby.rbenv import Rbenv
from eryx_deploy.assets.package_managers.ruby.ruby_gems_with_bundler import RubyGemsWithBundler
from eryx_deploy.assets.package_managers.frontend.npm import NPM
from eryx_deploy.assets.frameworks.abs_framework import FrameworkProject


class RubyOnRailsProject(FrameworkProject):
    def __init__(self, host_machine, project_name, db,
                 ruby_environment=Rbenv,
                 rails_env='production',
                 ruby_package_manager=RubyGemsWithBundler,
                 frontend_package_manager=NPM):
        super(RubyOnRailsProject, self).__init__(machine=host_machine, project_name=project_name)

        self._db = db

        self._ruby_environment = ruby_environment(host_machine=self._host_machine, ruby_version='2.3.4')
        self._ruby_environment.set_env_var('RAILS_ENV', rails_env)

        self._ruby_package_manager = ruby_package_manager(ruby_environment=self._ruby_environment)

        self._frontend_package_manager = frontend_package_manager(host_machine=self._host_machine)

    def first_time_setup(self):
        self._ruby_package_manager.first_time_setup()
        self._host_machine.upload_secrets_file()
        self._db.create()
        self._frontend_package_manager.first_time_setup()

        self.after_pull_update()

    def after_pull_update(self):
        self._ruby_package_manager.update_dependencies()
        self.migrate()
        self._frontend_package_manager.update_dependencies()
        self.compile_assets()

    def migrate(self):
        with self._cd_project():
            self._host_machine.create_db_dump_of(self._db)

        self._ruby_environment.run('rake db:migrate')

    def compile_assets(self):
        self._ruby_environment.run('rake assets:precompile')

    def _cd_project(self):
        return self._host_machine.cd_project()
