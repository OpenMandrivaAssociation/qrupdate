%define name	qrupdate
%define version 1.1.2
%define release %mkrel 1
%define major	1

%define libname %mklibname %name %major
%define develname %mklibname %name -d -s

Summary:	Fortran library for fast updates of QR/Cholesky decompositions
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	%{name}-%{version}.tar.gz
License:	GPLv3+
Group:		Development/Other
Url:		http://qrupdate.sourceforge.net/
BuildRequires:	gcc-gfortran, blas-devel, lapack-devel
Patch0:		qrupdate-1.1.1-Makefiles.patch

%description
qrupdate is a Fortran library for fast updates of QR and Cholesky
decompositions.

%package -n %{libname}
Summary:	qrupdate shared libraries
Group:		System/Libraries

%description -n %{libname}
qrupdate is a Fortran library for fast updates of QR and Cholesky
decompositions.

This package contains the shared library required for running programs
built against %{name}.

%package -n %{develname}
Summary:	qrupdate development files
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
qrupdate is a Fortran library for fast updates of QR and Cholesky
decompositions.

This package contains the files required for building programs
that use %{name}.

%prep
%setup -q
%patch0 -p1

sed -i Makeconf \
	-e "s:LIBDIR=lib:LIBDIR=%{_libdir}:" \
	-e "/^LIBDIR=/a\PREFIX=/" \
	-e "s:LAPACK=.*:LAPACK=$(pkg-config --libs lapack):" \
	-e "s:BLAS=.*:BLAS=$(pkg-config --libs blas):"


%build
#% make lib solib
%make

%install

#% ifarch x86_64
#% __sed -i 's,\/lib\/,\/lib64\/,g' src/Makefile
#% endif
#%make PREFIX=%{buildroot}/usr install
%makeinstall_std

%files -n %{libname}
%_libdir/*.so.*

%files -n %{develname}
%doc README ChangeLog COPYING
%_libdir/*.so
%_libdir/*.a
