#include "marketcapgui.h"
#include "ui_marketcapgui.h"

MarketCapgui::MarketCapgui(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MarketCapgui)
{
    ui->setupUi(this);
}

MarketCapgui::~MarketCapgui()
{
    delete ui;
}

