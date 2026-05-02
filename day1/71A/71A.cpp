#include <iostream>
using namespace std;

int main()
{
    int n;
    cin >> n;
    cin.ignore();
    string w;
    for (int i = 0; i < n; i++)
    {
        getline(cin, w);

        if (w.length() > 10)
        {
            cout << w.front() << w.length() - 2 << w.back() << endl;
        }
        else
        {
            cout << w << endl;
        }
    };

    return 0;
}