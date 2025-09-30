from typing import Optional, List
import json

class Dashboard:
    def __init__(self):
        self.title: Optional[str] = None
        self.charts: List[str] = []
        self.theme: str = "light"
        self.refresh: int = 30
        self.shared: bool = False

    def __str__(self):
        return json.dumps(self.__dict__, indent=2)

class DashboardComposer:
    def __init__(self):
        self._product = Dashboard()

    def set_title(self, title: str):
        if not title or not title.strip():
            raise ValueError("Title must be non-empty")
        self._product.title = title.strip()
        return self

    def add_chart(self, chart: str):
        if not chart or not chart.strip():
            raise ValueError("Chart name must be non-empty")
        self._product.charts.append(chart.strip())
        return self

    def use_dark_theme(self):
        self._product.theme = "dark"
        return self

    def use_light_theme(self):
        self._product.theme = "light"
        return self

    def enable_auto_refresh(self, seconds: int):
        if seconds < 5 or seconds > 3600:
            raise ValueError("Refresh interval must be 5-3600 seconds")
        self._product.refresh = seconds
        return self

    def share_publicly(self):
        self._product.shared = True
        return self

    def assemble(self) -> Dashboard:
        if not self._product.title:
            raise ValueError("Title is required")
        if not self._product.charts:
            raise ValueError("At least one chart is required")
        return self._product

class DashboardDirector:
    def create_sales_overview(self, composer: DashboardComposer) -> Dashboard:
        return (composer
                .set_title("Sales Overview")
                .add_chart("Revenue Trend")
                .add_chart("Units Sold")
                .use_dark_theme()
                .enable_auto_refresh(300)
                .share_publicly()
                .assemble())

    def create_analytics_summary(self, composer: DashboardComposer) -> Dashboard:
        return (composer
                .set_title("Analytics Summary")
                .add_chart("Page Views")
                .add_chart("Bounce Rate")
                .use_light_theme()
                .enable_auto_refresh(60)
                .assemble())

if __name__ == "__main__":
    composer = DashboardComposer()
    director = DashboardDirector()

    d1 = director.create_sales_overview(composer)
    print(d1)

    d2 = (composer
          .set_title("Custom Dashboard")
          .add_chart("CPU Usage")
          .add_chart("Memory Load")
          .enable_auto_refresh(10)
          .assemble())
    print(d2)