#include <iostream>
using namespace std;

int main()
{

    string w;
    cin >> w;
    string out_put_str;
    for (int i = 0; i < w.length(); i++)
    {
        char c = w[i];

        if (c >= 'A' && c <= 'Z')
        {
            c += 32;
        };
        if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u' || c=='y')
        {
            continue;
        }

        out_put_str += ".";
        out_put_str += c;
    };
    cout << out_put_str << endl;
    return 0;
}