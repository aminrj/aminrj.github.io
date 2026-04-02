#!/usr/bin/env ruby

begin
  if ARGV.include?("serve")
    require "webrick/httpserver"

    module WEBrickConnresetPatch
      def run(socket, *args)
        super
      rescue Errno::ECONNRESET, Errno::EPIPE
        # Ignore browser disconnect noise during local development.
      end
    end

    WEBrick::HTTPServer.prepend(WEBrickConnresetPatch)
  end
rescue LoadError
  # WEBrick is only loaded for local serving.
end