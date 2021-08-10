#include "marketcapgui.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MarketCapgui w;
    w.show();
    return a.exec();
}
