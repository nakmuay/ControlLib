pkg load control;

f = fopen("../sim.txt");
C = textscan(f, "%s %s %s %s", 1);
simDat = textscan(f, "%f %f %f %f", "delimiter", " ");
fclose(f);

t = simDat{1};
u = simDat{2};
y = simDat{3};
y_sim = simDat{4};

dat = iddata(y, u);

na = 4;
nb = 4;
tf_sys = arx(dat, "na", na, "nb", nb);
[sys, x0] = arx(dat, "na", na, "nb", nb);

y_ref = lsim(sys, u, t, x0);

figure();
plot(t, y, "b", "linewidth", 2);
hold on;
plot(t, y_sim, "g.-", "linewidth", 2);
plot(t, y_ref, "r.-", "linewidth", 2);

