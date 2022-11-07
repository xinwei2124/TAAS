clear; clc; close all    
    
Matrix = load("Matrix.csv");
Matrix = Matrix';

presto_high_cost = load("PRESTO_high_cost.csv");
presto_high_cost = presto_high_cost';

presto_low_cost = load("PRESTO_low_cost.csv");
presto_low_cost = presto_low_cost';


Matrix_noise1 = load("Matrix_noise1.csv");
Matrix_noise1 = Matrix_noise1';

presto_high_cost_noise1 = load("PRESTO_high_cost_noise1.csv");
presto_high_cost_noise1 = presto_high_cost_noise1';

presto_low_cost_noise1 = load("PRESTO_low_cost_noise1.csv");
presto_low_cost_noise1 = presto_low_cost_noise1';


Matrix_noise2 = load("Matrix_noise1.csv");
Matrix_noise2 = Matrix_noise2';

presto_high_cost_noise2 = load("PRESTO_high_cost_noise2.csv");
presto_high_cost_noise2 = presto_high_cost_noise2';

presto_low_cost_noise2 = load("PRESTO_low_cost_noise2.csv");
presto_low_cost_noise2 = presto_low_cost_noise2';


violation_matrix = nan(20,44);
counter = 0;
for i=1:11
    counter = counter +1;
    violation_matrix(:,counter)=Matrix(:,i);
    counter = counter +1;
    violation_matrix(:,counter)=presto_high_cost(:,i);
    counter = counter +1;
    violation_matrix(:,counter)=presto_high_cost_noise1(:,i);
    counter = counter +1;
    violation_matrix(:,counter)=presto_high_cost_noise2(:,i);
end
figure;
positions = [1 2 3 4 6 7 8 9 11 12 13 14 16 17 18 19 21 22 23 24 26 27 28 29 31 32 33 34 36 37 38 39 41 42 43 44 46 47 48 49 51 52 53 54];
boxplot(violation_matrix, 'positions', positions, 'widths', 0.85);
ylim([-0.1 21])
h=gca; 
h.XAxis.TickLength = [0 0];
set(gca,'xtick',[mean(positions(1:4)) mean(positions(5:8)) mean(positions(9:12)) mean(positions(13:16)) mean(positions(17:20)) mean(positions(21:24)) mean(positions(25:28)) mean(positions(29:32)) mean(positions(33:36))  mean(positions(37:40)) mean(positions(41:44))]);
set(gca,'xticklabel',{'0', '5', '10', '15', '20', '25', '30', '35', '40', '45', '50'});

color = ['r', 'b', 'm', 'c','r', 'b', 'm', 'c','r', 'b', 'm', 'c','r', 'b', 'm', 'c','r', 'b', 'm', 'c','r', 'b', 'm', 'c','r', 'b', 'm', 'c','r', 'b', 'm', 'c','r', 'b', 'm', 'c','r', 'b', 'm', 'c','r', 'b', 'm', 'c'];
h = findobj(gca,'Tag','Box');
for j=1:length(h)
    patch(get(h(j),'XData'),get(h(j),'YData'),color(j),'FaceAlpha',.5);
end

tickSize = get(gca,'XTickLabel');
set(gca,'XTickLabel',tickSize,'fontsize',19)
tickSize = get(gca,'YTickLabel');
set(gca,'YTickLabel',tickSize,'fontsize',17)

yl = ylim(); % Find out x location of the y axis.
% Cover up existing axis with a white line.
line([0 0.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([4.5 5.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([9.5 10.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([14.5 15.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([19.5 20.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([24.5 25.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([29.5 30.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([34.5 35.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([39.5 40.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([44.5 45.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([49.5 50.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
% hold on
% line([54.5 55.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 2);

legend('High noise','low noise','noise free','Baseline','fontsize',18,'edgecolor','w'); 
hAx=gca;                             
hAx.XTickLabel=hAx.XTickLabel;
xlabel("Number of regular services (in a year)","FontSize",20);
ylabel("Number of disruptions","FontSize",20);
% set(gca,'ygrid','on')
% title("Increasing fixed interval serive reduces disruptions","FontSize",12)

% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Matrix = load("Matrix.csv");
Matrix = Matrix';

presto_high_cost = load("PRESTO_high_cost.csv");
presto_high_cost = presto_high_cost';

presto_low_cost = load("PRESTO_low_cost.csv");
presto_low_cost = presto_low_cost';


Matrix_noise1 = load("Matrix_noise1.csv");
Matrix_noise1 = Matrix_noise1';

presto_high_cost_noise1 = load("PRESTO_high_cost_noise1.csv");
presto_high_cost_noise1 = presto_high_cost_noise1';

presto_low_cost_noise1 = load("PRESTO_low_cost_noise1.csv");
presto_low_cost_noise1 = presto_low_cost_noise1';


Matrix_noise2 = load("Matrix_noise2.csv");
Matrix_noise2 = Matrix_noise2';

presto_high_cost_noise2 = load("PRESTO_high_cost_noise2.csv");
presto_high_cost_noise2 = presto_high_cost_noise2';

presto_low_cost_noise2 = load("PRESTO_low_cost_noise2.csv");
presto_low_cost_noise2 = presto_low_cost_noise2';


cost_rate = 2;
c0 = 10;

violation_matrix = nan(20,44);
counter = 0;

for i=1:11
    counter = counter +1;
    %cost for baseline
    a = (i-1)*5;
    violation_matrix(:,counter) = (Matrix(:,i)*(cost_rate) + a)*c0;
%     violation_matrix(:,counter) = (Matrix(:,i)*(cost_rate) + (i-1)*20)*c0;
    counter = counter +1;
    %cost for PRESTO
    violation_matrix(:,counter)=(presto_high_cost(:,i)*(cost_rate)+presto_low_cost(:,i))*c0;
    counter = counter +1;
    %cost for PRESTO noise low
    violation_matrix(:,counter)=(presto_high_cost_noise1(:,i)*(cost_rate)+presto_low_cost_noise1(:,i))*c0;
    counter = counter +1;
    %cost for PRESTO noise low
    violation_matrix(:,counter)=(presto_high_cost_noise2(:,i)*(cost_rate)+presto_low_cost_noise2(:,i))*c0;
end
figure;
positions = [1 2 3 4 6 7 8 9 11 12 13 14 16 17 18 19 21 22 23 24 26 27 28 29 31 32 33 34 36 37 38 39 41 42 43 44 46 47 48 49 51 52 53 54];
boxplot(violation_matrix, 'positions', positions, 'widths', 0.85);
h=gca; 
h.XAxis.TickLength = [0 0];
set(gca,'xtick',[mean(positions(1:4)) mean(positions(5:8)) mean(positions(9:12)) mean(positions(13:16)) mean(positions(17:20)) mean(positions(21:24)) mean(positions(25:28)) mean(positions(29:32)) mean(positions(33:36))  mean(positions(37:40)) mean(positions(41:44))]);
set(gca,'xticklabel',{'0', '5', '10', '15', '20', '25', '30', '35', '40', '45', '50'});

color = ['r', 'b', 'm', 'c','r', 'b', 'm', 'c','r', 'b', 'm', 'c','r', 'b', 'm', 'c','r', 'b', 'm', 'c','r', 'b', 'm', 'c','r', 'b', 'm', 'c','r', 'b', 'm', 'c','r', 'b', 'm', 'c','r', 'b', 'm', 'c','r', 'b', 'm', 'c'];
h = findobj(gca,'Tag','Box');
for j=1:length(h)
    patch(get(h(j),'XData'),get(h(j),'YData'),color(j),'FaceAlpha',.5);
end

tickSize = get(gca,'XTickLabel');
set(gca,'XTickLabel',tickSize,'fontsize',19)
tickSize = get(gca,'YTickLabel');
set(gca,'YTickLabel',tickSize,'fontsize',17)

yl = ylim(); % Find out x location of the y axis.
% Cover up existing axis with a white line.
line([0 0.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([4.5 5.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([9.5 10.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([14.5 15.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([19.5 20.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([24.5 25.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([29.5 30.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([34.5 35.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([39.5 40.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([44.5 45.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
hold on
line([49.5 50.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 3);
% hold on
% line([54.5 55.5], [yl(1), yl(1)], 'color', 'w', 'LineWidth', 2);

legend('High noise','low noise','noise free','Baseline','fontsize',18,'edgecolor','w','Location','southeast'); 
hAx=gca;                             
hAx.XTickLabel=hAx.XTickLabel;
xlabel("Number of regular services (in a year)","FontSize",20);
ylabel("Cost","FontSize",20);
% set(gca,'ygrid','on')
% title("The cost of preventitive service is 2 times cheaper than the urgent service","FontSize",12)
