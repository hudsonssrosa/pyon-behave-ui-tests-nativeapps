module Fastlane
  module Actions
    module SharedValues
      CHECK_FOR_TAG_CUSTOM_VALUE = :CHECK_FOR_TAG_CUSTOM_VALUE
    end

    class CheckForTagAction < Action
      def self.run(params)
        sh('git fetch --tags')
        tag = sh('git describe --tags --abbrev=0 ')
        tag_commit_hash = sh("git show-ref -s #{tag}")
        current_commit_hash = sh('git rev-parse HEAD')
        UI.message "Last tag is: #{tag} with commit hash #{tag_commit_hash}"
        UI.message "Current commit hash is: #{current_commit_hash}"
        tag_commit_hash == current_commit_hash
      end

      #####################################################
      # @!group Documentation
      #####################################################

      def self.description
        "Checks if the current commit is tagged for release"
      end

      def self.details
        # Optional:
        # this is your chance to provide a more detailed description of this action
        ""
      end

      def self.available_options
        []
      end

      def self.output

        [
        ]
      end

      def self.return_value
        "Returns true if the current commit is tagged for release"
      end

      def self.authors
        # So no one will ever forget your contribution to fastlane :) You are awesome btw!
        [""]
      end

      def self.is_supported?(platform)
        true
      end
    end
  end
end
