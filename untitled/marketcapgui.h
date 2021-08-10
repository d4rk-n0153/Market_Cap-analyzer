#ifndef MARKETCAPGUI_H
#define MARKETCAPGUI_H

#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui { class MarketCapgui; }
QT_END_NAMESPACE

class MarketCapgui : public QMainWindow
{
    Q_OBJECT

public:
    MarketCapgui(QWidget *parent = nullptr);
    ~MarketCapgui();

private:
    Ui::MarketCapgui *ui;
};
#endif // MARKETCAPGUI_H
