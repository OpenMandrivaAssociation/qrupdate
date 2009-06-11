%define name	qrupdate
%define version 1.0.1
%define release %mkrel 2
%define major	1

%define libname %mklibname %name %major
%define develname %mklibname %name -d

Summary:	Fortran library for fast updates of QR/Cholesky decompositions
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	%{name}-%{version}.tar.gz
License:	GPLv3+
Group:		Development/Other
Url:		http://qrupdate.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	gcc-gfortran, blas-devel, lapack-devel

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

%build
%make lib solib

%install
%__rm -rf %{buildroot}

%ifarch x86_64
%__sed -i 's,\/lib\/,\/lib64\/,g' src/Makefile
%endif
%make PREFIX=%{buildroot}/usr install

%clean
%__rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%_libdir/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%doc README ChangeLog COPYING
%_libdir/*.so
%_libdir/*.a

