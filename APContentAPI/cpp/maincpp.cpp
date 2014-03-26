#include <iostream>
#include <sstream>
#include <string>
#include <exception>

#include "boost\program_options.hpp"
#include "boost\format.hpp"
#include "boost\property_tree\ptree.hpp"
#include "boost\property_tree\json_parser.hpp"
#include "boost\foreach.hpp"

#include "cpprest/http_client.h"
#include "cpprest/json.h"

using namespace utility;                    // Common utilities like string conversions
using namespace web;                        // Common features like URIs.
using namespace web::http;                  // Common HTTP functionality
using namespace web::http::client;          // HTTP client features
using namespace concurrency::streams;       // Asynchronous streams

using namespace boost::property_tree;
namespace pt = boost::property_tree;
using namespace boost::program_options;
namespace po = boost::program_options;

int main(int argc, char* argv[])
{
	utility::string_t api_key(U("** Your API Key here **"));
	
	// Declare the supported options.
	po::options_description desc("Allowed options");
	desc.add_options()
		("help", "produce help message")
		("media_type,m", po::value<std::string>()->default_value("photo"), "set media type")
		("query,q", po::value<std::string>()->required(), "set search query")
	;
	positional_options_description pd;
	pd.add("media_type", 1).add("query", 1);

	po::variables_map var_map;
	po::store(po::parse_command_line(argc, argv, desc), var_map);
	po::store(po::command_line_parser(argc, argv).
		options(desc).positional(pd).run(), var_map);

	if (var_map.count("help")) {
		std::cout << desc << "\n";
		return 1;
	}

	try {
		po::notify(var_map);    
	}
	catch (std::exception &e) {
		std::cerr << "Caught exception while parsing command line options:" << e.what() << "\n";
		return 1;
	}

	// Create http_client to send the request.
	http_client api_client(U("http://api.ap.org/v2/search/"));

	// Set accept header for output format
	http_request api_request(methods::GET);
	api_request.headers().add(web::http::header_names::accept, U("application/json"));

	// Build request URI and start the request.
	utility::string_t media_type_param = U("/") + utility::conversions::to_string_t(var_map["media_type"].as<std::string>());
	uri_builder builder(media_type_param);
	builder.append_query(U("apikey"), api_key);
	builder.append_query(U("q"), utility::conversions::to_string_t(var_map["query"].as<std::string>()));
	api_request.set_request_uri(builder.to_string());

	// Initiate the request and process the response
	pplx::task<std::string> requestTask = api_client.request(api_request).then([](http_response response)
	{
		if (response.status_code() == status_codes::OK)
		{
			return response.extract_string();
		}

		// Handle error cases, for now return empty string value... 
		return pplx::task_from_result(utility::string_t());
	})
	.then([](pplx::task<utility::string_t> previousTask)
	{
		const utility::string_t &body_text = previousTask.get();
		std::string json_text = utility::conversions::to_utf8string(body_text);
		return pplx::task_from_result(json_text.substr(3, json_text.length() - 3));
	});

	// Wait for all the outstanding I/O to complete and handle any exceptions
	std::string response_body;
	try
	{
		response_body = requestTask.get();
	}
	catch (const std::exception &e)
	{
		printf("Error exception: %s\n", e.what());
	}

	// Hack to skip byte order mark the to_utf8string() adds
	std::istringstream body_stream(response_body);
	pt::ptree parsed_body;
	pt::read_json(body_stream, parsed_body);

	// Output the results in a simplified manner
	std::cout << "Total Found = " << parsed_body.get<std::string>("totalResults") << std::endl;

	// Content entries
	BOOST_FOREACH(ptree::value_type &entry, parsed_body.get_child("entries"))
	{
		std::cout << "Title: " << entry.second.get<std::string>("title") << std::endl;
	}

	puts("Hit any key to exit...");
	std::cin.get();
	return 0;
}