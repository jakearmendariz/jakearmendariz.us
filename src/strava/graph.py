 def graph_activity_distribution(self, line = None):
        fig, ax = self.init_graph()
        if line != None and line == "smooth":
            self.get_activity_smooth_line(ax=ax)
            return mpld3.fig_to_html(fig)
        else:
            line = self.get_activity_line()
            line.plot(linewidth=2.5)
            return mpld3.fig_to_html(fig)
    
    def init_graph(self):
        plt.switch_backend('Agg')
        plt.ylabel('miles')
        plt.xlabel('time')
        plt.title('Distance over time')
        fig, ax = plt.subplots(figsize=(8, 4))
        return fig, ax
        
    def get_activity_line(self):
        dates, distances = self.get_dates_and_distances()
        return pd.Series(data=np.array(distances), index=np.array(dates))

    
    def get_activity_smooth_line(self, fig = None, ax = ax):
        dates, distances = self.get_dates_and_distances()
        x = self.turn_dates_into_numbers(dates)
        x_new = np.linspace(x[0], x[-1],2000)
        f = interp1d(x, distances, kind='quadratic')
        y_smooth=f(x_new)
        ax.plot (x_new,y_smooth, label="pace")
    
    def get_dates_and_distances(self, before_date = "2020-07-29T00:00:00Z"):
        activities = self.client.get_activities(before = before_date,  limit=1000)
        distances, dates = [], []
        for activity in activities:
            activity = activity.to_dict()
            dates.append(activity['start_date_local'])
            distances.append(self.to_miles(activity))
        return np.array(dates), np.array(distances)
    
    def turn_dates_into_numbers(self, dates):
        return np.arange(len(dates))