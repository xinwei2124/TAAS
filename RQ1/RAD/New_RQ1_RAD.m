clear; clc; close all    
    
Matrix = load("Matrix.csv");
Matrix = Matrix';

presto_high_cost = load("PRESTO_high_cost.csv");
presto_high_cost = presto_high_cost';

violation_matrix = nan(20,22);
counter = 0;
for i=1:11
    counter = counter +1;
    violation_matrix(:,counter)=Matrix(:,i);
    counter = counter +1;
    violation_matrix(:,counter)=presto_high_cost(:,i);
end
figure;
positions = [1 2 4 5 7 8 10 11 13 14 16 17 19 20 22 23 25 26 28 29 31 32];
boxplot(violation_matrix, 'positions', positions, 'widths', 0.85);
ylim([0 25])
h=gca; 
h.XAxis.TickLength = [0 0];
set(gca,'xtick',[mean(positions(1:2)) mean(positions(3:4)) mean(positions(5:6)) mean(positions(7:8)) mean(positions(9:10)) mean(positions(11:12)) mean(positions(13:14)) mean(positions(15:16)) mean(positions(17:18))  mean(positions(19:20)) mean(positions(21:22))]);
set(gca,'xticklabel',{'0', '5', '10', '15', '20', '25', '30', '35', '40', '45', '50'});

color = ['m', 'c', 'm', 'c', 'm', 'c', 'm', 'c', 'm', 'c', 'm', 'c', 'm', 'c', 'm', 'c', 'm', 'c', 'm', 'c', 'm', 'c'];
h = findobj(gca,'Tag','Box');
for j=1:length(h)
    patch(get(h(j),'XData'),get(h(j),'YData'),color(j),'FaceAlpha',.5);
end

tickSize = get(gca,'XTickLabel');
set(gca,'XTickLabel',tickSize,'fontsize',20)
tickSize = get(gca,'YTickLabel');
set(gca,'YTickLabel',tickSize,'fontsize',20)


yl = ylim(); % Find out x location of the y axis.
% Cover up existing axis with a white line.
line([0 0.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([2.5 3.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([5.5 6.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([8.5 9.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([11.5 12.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([14.5 15.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([17.5 18.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([20.5 21.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([23.5 24.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([26.5 27.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([29.5 30.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([32.5 33], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);

legend('PRESTO','Baseline','fontsize',28,'edgecolor','w'); 
hAx=gca;                             
hAx.XTickLabel=hAx.XTickLabel;
xlabel("Number of regular services (in a year)","FontSize",28);
ylabel("Number of disruptions","FontSize",28);

% % %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
figure;

Matrix = load("Matrix.csv");
Matrix = Matrix';

presto_high_cost_frt = load("PRESTO_high_cost.csv");
presto_high_cost_frt = presto_high_cost_frt';

presto_low_cost_frt = load("PRESTO_low_cost.csv");
presto_low_cost_frt = presto_low_cost_frt';

violation_matrix = nan(20,22);
counter = 0;

cost_rate = 2;
c0 = 10;

for i=1:11
    counter = counter +1;
    %cost for baseline
    a = (i-1)*5;
    violation_matrix(:,counter) = (Matrix(:,i)*(cost_rate) + a)*c0;
    counter = counter +1;
    %cost for PRESTO
    violation_matrix(:,counter)=(presto_high_cost_frt(:,i)*(cost_rate)+presto_low_cost_frt(:,i))*c0;
end

positions = [1 2 4 5 7 8 10 11 13 14 16 17 19 20 22 23 25 26 28 29 31 32];
boxplot(violation_matrix, 'positions', positions, 'widths', 0.85);
h=gca; 
h.XAxis.TickLength = [0 0];
set(gca,'xtick',[mean(positions(1:2)) mean(positions(3:4)) mean(positions(5:6)) mean(positions(7:8)) mean(positions(9:10)) mean(positions(11:12)) mean(positions(13:14)) mean(positions(15:16)) mean(positions(17:18))  mean(positions(19:20)) mean(positions(21:22))]);
set(gca,'xticklabel',{'0', '5', '10', '15', '20', '25', '30', '35', '40', '45', '50'});

color = ['m', 'c', 'm', 'c', 'm', 'c', 'm', 'c', 'm', 'c', 'm', 'c', 'm', 'c', 'm', 'c', 'm', 'c', 'm', 'c', 'm', 'c'];
h = findobj(gca,'Tag','Box');
for j=1:length(h)
    patch(get(h(j),'XData'),get(h(j),'YData'),color(j),'FaceAlpha',.5);
end

tickSize = get(gca,'XTickLabel');
set(gca,'XTickLabel',tickSize,'fontsize',20)
tickSize = get(gca,'YTickLabel');
set(gca,'YTickLabel',tickSize,'fontsize',20)

yl = ylim(); % Find out x location of the y axis.
% Cover up existing axis with a white line.
line([0 0.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([2.5 3.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([5.5 6.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([8.5 9.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([11.5 12.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([14.5 15.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([17.5 18.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([20.5 21.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([23.5 24.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([26.5 27.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([29.5 30.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([32.5 33], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);

legend('PRESTO','Baseline','fontsize',28,'edgecolor','w'); 
hAx=gca;                             
hAx.XTickLabel=hAx.XTickLabel;
xlabel("Number of regular services (in a year)","FontSize",28);
ylabel("Cost","FontSize",28);
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
figure;

Matrix = load("Matrix.csv");
Matrix = Matrix';

presto_high_cost_frt = load("PRESTO_high_cost.csv");
presto_high_cost_frt = presto_high_cost_frt';

presto_low_cost_frt = load("PRESTO_low_cost.csv");
presto_low_cost_frt = presto_low_cost_frt';

violation_matrix = nan(20,22);
counter = 0;

cost_rate = 3;
c0 = 10;

for i=1:11
    counter = counter +1;
    %cost for baseline
    a = (i-1)*5;
    violation_matrix(:,counter) = (Matrix(:,i)*(cost_rate) + a)*c0;
    counter = counter +1;
    %cost for PRESTO
    violation_matrix(:,counter)=(presto_high_cost_frt(:,i)*(cost_rate)+presto_low_cost_frt(:,i))*c0;
end

positions = [1 2 4 5 7 8 10 11 13 14 16 17 19 20 22 23 25 26 28 29 31 32];
boxplot(violation_matrix, 'positions', positions, 'widths', 0.85);
h=gca; 
h.XAxis.TickLength = [0 0];
set(gca,'xtick',[mean(positions(1:2)) mean(positions(3:4)) mean(positions(5:6)) mean(positions(7:8)) mean(positions(9:10)) mean(positions(11:12)) mean(positions(13:14)) mean(positions(15:16)) mean(positions(17:18))  mean(positions(19:20)) mean(positions(21:22))]);
set(gca,'xticklabel',{'0', '5', '10', '15', '20', '25', '30', '35', '40', '45', '50'});

color = ['m', 'c', 'm', 'c', 'm', 'c', 'm', 'c', 'm', 'c', 'm', 'c', 'm', 'c', 'm', 'c', 'm', 'c', 'm', 'c', 'm', 'c'];
h = findobj(gca,'Tag','Box');
for j=1:length(h)
    patch(get(h(j),'XData'),get(h(j),'YData'),color(j),'FaceAlpha',.5);
end

tickSize = get(gca,'XTickLabel');
set(gca,'XTickLabel',tickSize,'fontsize',20)
tickSize = get(gca,'YTickLabel');
set(gca,'YTickLabel',tickSize,'fontsize',20)

yl = ylim(); % Find out x location of the y axis.
% Cover up existing axis with a white line.
line([0 0.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([2.5 3.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([5.5 6.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([8.5 9.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([11.5 12.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([14.5 15.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([17.5 18.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([20.5 21.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([23.5 24.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([26.5 27.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([29.5 30.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([32.5 33], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);

legend('PRESTO','Baseline','fontsize',28,'edgecolor','w'); 
hAx=gca;                             
hAx.XTickLabel=hAx.XTickLabel;
xlabel("Number of regular services (in a year)","FontSize",28);
ylabel("Cost","FontSize",28);
