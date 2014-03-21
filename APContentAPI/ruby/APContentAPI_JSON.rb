require "rubygems"
require "json"
require "net/http"
require "uri"
require "open-uri"

# Sign up for your apiKey at http://developer.ap.org
apiKey = "xxxxxx"

# Check to see if the download folder exists. If not create it.
begin
  downloadDir = "~/APContentAPI"
  unless File.exists? File.expand_path(downloadDir)
          Dir.mkdir File.expand_path(downloadDir)
        end
      rescue => e
        puts "#{e}"
  end

# Enter search criteria
puts "What media type are you looking for?"
puts "Valid values are: photo, graphic and video. Please pick one."
mediaType = gets.chomp
puts "What would you like to search for?"
keywordSearch = gets.chomp 

# Make the AP ContentAPI request and escape whitespace
begin
  apiURL = "http://api.ap.org/v2/search/#{mediaType}?q=#{keywordSearch}&apiKey=#{apiKey}"
  uri = URI.parse(apiURL.gsub(/ /, '+'))
  puts "Searching #{uri}"

  http = Net::HTTP.new(uri.host, uri.port)
  request = Net::HTTP::Get.new(uri.request_uri, {'Accept' => 'application/json'})
  response = http.request(request)  
  puts "Status Code: #{response.code}"

  result = JSON.parse(response.body[3..-1].force_encoding("UTF-8"))
  puts "Total Results: #{result['totalResults']}"
  puts "Items Per Page: #{result['itemsPerPage']}"

rescue => e
  puts "#{e}"
end

# Loop through each item's link and save the preview item
if result['totalResults'] >= 1
  result['entries'].each { |entry|
    begin
      puts entry['title']

      entry['contentLinks'].each { |contentLink|
        if contentLink['rel'] == "preview"

          # Get the suggested filename from the link
          fileName = contentLink['href']
          fileName = fileName.sub( /^http.*filename=*/, '')
          fileName = fileName.sub( /&sid.*$/, '')

          bapiURL = contentLink['href'] + "&apiKey=" + apiKey
          puts "Downloading #{bapiURL}"
          
          # Using open-uri here to download the binary because it automatically supports redirects which is mandatory for the AP Content API
          bapiRemoteFile = open(bapiURL).read {|f| f.each_line
            p f.status
            }

          bapiLocalfile = File.open(File.expand_path(downloadDir) + "/" + fileName, "w") 
          bapiLocalfile.write(bapiRemoteFile)
          bapiLocalfile.close
        end
      }
    rescue => e
      puts "#{e}"
    end
  }

else
  puts "Please try another search..."
end