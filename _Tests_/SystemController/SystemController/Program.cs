using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Sharp7;

namespace SystemController
{
    class Program
    {
        static void Main(string[] args)
        {
            string plc_ip = "192.168.125.2";
            var client = new S7Client();
            int result = client.ConnectTo(plc_ip, 0, 1);
            
            if(result == 0)
            {
                Console.WriteLine("Connection established with " + plc_ip +"!");
            }
            else
            {
                Console.WriteLine("Connection failed with " + plc_ip + "!");
                return; 
            }

            Console.WriteLine("Write to DB");


            Console.WriteLine("Press enter to exit!");
            Console.ReadLine();
            client.Disconnect();
        }
    }
}
