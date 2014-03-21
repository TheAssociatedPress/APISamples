using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml.Linq;



namespace AP.APISamples
{
    class APIClient
    {
        static void Main(string[] args)
        {
            // sign up for developer key at http://developer.ap.org/
            var apikey = "** your api key **";

            var keyword_search = "star wars";

            var payload = XElement.Load(string.Format(@"http://api.ap.org/v2/search?count=1&apikey={0}&q={1}", 
                apikey, System.Web.HttpUtility.UrlEncode(keyword_search)));

            XNamespace ns = "http://www.w3.org/2005/Atom";

            var suggested_term = (from s in payload.Elements(ns + "link")
                                 where s.Attribute("rel").Value == "suggestedTerm"
                                 select s.Attribute("title")).FirstOrDefault().Value;

            System.Console.WriteLine("suggested term: \"{0}\"", suggested_term);

            var first_entry = payload.Element(ns + "entry");

            System.Console.WriteLine("title of the most recent image about \"{0}\" is \"{1}\"", keyword_search, first_entry.Element(ns + "title").Value);

            var img_url = (from u in first_entry.Elements(ns + "link")
                                 where u.Attribute("rel").Value == "thumbnail"
                                 select u.Attribute("href")).FirstOrDefault().Value;

            System.Console.WriteLine("downloading thumbnail link {0}", img_url);

            (new System.Net.WebClient()).DownloadFile(img_url + string.Format("&apikey={0}", apikey), @"c:\temp\thumbnail.jpg");
        }
    }
}
